from api import GitHubAPI

from .async_worker import AsyncWorker


class AsyncOrganizationWorker(AsyncWorker):
    def __init__(self, number_of_organization: int, api: GitHubAPI):
        super().__init__(api)
        self.number_of_organization: int = number_of_organization

        self.url_organizations: str = "https://api.github.com/organizations"
        self.maximum_number_of_organizations_per_request: int = 100
        self.organizations_with_repository_urls: dict[int, str] = dict()

    async def get_data(self, *args, **kwargs) -> list[str]:
        if self.number_of_organization <= self.maximum_number_of_organizations_per_request:
            await self.update_organization_data(per_page=self.number_of_organization)
        else:
            for _ in range(self.number_of_organization // self.maximum_number_of_organizations_per_request):
                await self.update_organization_data()

            remain = self.number_of_organization % self.maximum_number_of_organizations_per_request
            if remain != 0:
                await self.update_organization_data(per_page=remain)

        return list(self.organizations_with_repository_urls.values())

    async def update_organization_data(self, per_page: int = 100) -> None:
        params = {"per_page": per_page, "since": self.since}
        response = await self.api.get(self.url_organizations, params=params)
        data = {org["id"]: org["repos_url"] for org in response}
        self.organizations_with_repository_urls.update(data)

    @property
    def since(self) -> int:
        return list(self.organizations_with_repository_urls.keys())[-1] \
            if self.organizations_with_repository_urls else 0

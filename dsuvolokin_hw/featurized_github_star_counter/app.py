from _settings import mode

if mode == 'async':
	from async_pipeline import main
elif mode == 'm_thr':
	from m_thread_pipeline import main
elif mode == 'm_prc':
	from m_proc_pipeline import main

if __name__ == '__main__':
  main()
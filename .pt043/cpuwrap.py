"""cpuwrap.py [main.py (default: ./c3-main.py)] : run main.py unchanged, log CPU (process_time) per /move to $CPU_LOG.
Patches urllib.request.urlopen only to timestamp requests; engine code is exec'd as-is."""
import sys, time, runpy, urllib.request as U
log = open(__import__('os').environ['CPU_LOG'], 'w')
_orig = U.urlopen
st = {'t': None, 'n': 0}
def urlopen(req, *a, **k):
    now = time.process_time()
    url = req.full_url if hasattr(req, 'full_url') else str(req)
    if url.endswith('/move') and st['t'] is not None:
        st['n'] += 1
        log.write(f"{st['n']}\t{now - st['t']:.4f}\n"); log.flush()
    r = _orig(req, *a, **k)
    st['t'] = None
    class W:
        def __init__(s, r): s.r = r
        def read(s, *x):
            d = s.r.read(*x); st['t'] = time.process_time(); return d
        def __getattr__(s, n): return getattr(s.r, n)
        def __enter__(s): return s
        def __exit__(s, *e): s.r.close()
    return W(r)
U.urlopen = urlopen
import os
sys.argv = [sys.argv[1] if len(sys.argv) > 1 else os.environ.get('ENGINE') or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'c3-main.py')]
runpy.run_path(sys.argv[0], run_name='__main__')

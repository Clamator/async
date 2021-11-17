import threading

lock_obj = threading.RLock()

print('acquire 1st time')
lock_obj.acquire()
lock_obj.release()
print('acquire 2nd time')
lock_obj.acquire()

print('releasing')
lock_obj.release()

#def reentrance():
#    print('start')
#    lock_obj.acquire()
#    print('acquired')
#    reentrance()
#
#reentrance()
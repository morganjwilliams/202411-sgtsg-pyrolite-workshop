def mpl_usr_tmp(instance):
  import os
  return os.path.expanduser('~' + instance.user.name + '/.mpl')

def nb_usr_tmp(instance):
  import os
  return os.path.expanduser('~' + instance.user.name + '/.numba')

c.Spawner.environment.update({ "MPLCONFIGDIR":  mpl_usr_tmp, "NUMBA_CACHE_DIR": nb_usr_tmp})
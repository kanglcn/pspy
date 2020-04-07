import os, sys
import numpy as np

from scipy.io import loadmat, savemat
from getparm import get_parm_value as getparm


def ps_unwrap():
    print('Phase-unwrapping...\n')

    small_baseline_flag = getparm('small_baseline_flag')[0][0]
    unwrap_patch_phase = getparm('unwrap_patch_phase')[0][0]
    scla_deramp = getparm('scla_deramp')[0][0]
    subtr_tropo = getparm('subtr_tropo')[0][0]
    aps_name = getparm('tropo_method')[0][0]

    psver = loadmat('psver.mat')['psver'][0][0]
    psname = 'ps' + str(psver)
    rcname = 'rc' + str(psver)
    pmname = 'pm' + str(psver)
    bpname = 'bp' + str(psver)
    goodname = 'phuw_good' + str(psver)

    if small_baseline_flag != 'y':
        sclaname = 'scla_smooth' + str(psver)
        apsname = 'tca' + str(psver)
        phuwname = 'phuw' + str(psver)
    else:
        print("You set the param small_baseline_flag={}, but not supported yet.".format(
            getparm('small_baseline_flag')[0][0]))
        sys.exit()
        # sclaname=['scla_smooth_sb',num2str(psver)];
        # apsname=['tca_sb',num2str(psver)];
        # phuwname=['phuw_sb',num2str(psver),'.mat'];

    ps = loadmat(psname + '.mat');

    drop_ifg_index = getparm('drop_ifg_index')[0]
    unwrap_ifg_index = np.setdiff1d(np.arange(0, ps['n_ifg'][0][0]), drop_ifg_index)

    bp = {}
    if os.path.exists(bpname + '.mat'):
        bp = loadmat(bpname + '.mat')
    else:
        bperp = ps['bperp']
        if small_baseline_flag != 'y':
            bperp = np.concatenate((bperp[:ps['master_ix'][0][0] - 1], bperp[ps['master_ix'][0][0]:]), axis=0)
        bp['bperp_mat'] = np.tile(bperp.T, (ps['n_ps'][0][0], 1))

    if small_baseline_flag!='y':
        bperp_mat=[bp.bperp_mat(:,1:ps.master_ix-1),zeros(ps.n_ps,1,'single'),bp.bperp_mat(:,ps.master_ix:end)];
    else:
        print("You set the param small_baseline_flag={}, but not supported yet.".format(
            getparm('small_baseline_flag')[0][0]))
        sys.exit()
        # bperp_mat=bp.bperp_mat;

    print()

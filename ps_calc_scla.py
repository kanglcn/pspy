import sys, os
import numpy as np
from inspect import signature
from scipy.io import loadmat
from ps_deramp import ps_deramp
from ps_setref import ps_setref
from getparm import get_parm_value as getparm


def ps_calc_scla(use_small_baselines, coest_mean_vel):
    print('');
    print('Estimating spatially-correlated look angle error...')

    sig = signature(ps_calc_scla)
    args = sig.parameters
    if len(args) < 1:
        use_small_baselines = 0;
    if len(args) < 2:
        coest_mean_vel = 0;

    # TODO: Implement getparm() function
    small_baseline_flag = getparm('small_baseline_flag')[0][0]
    drop_ifg_index = getparm('drop_ifg_index')[0]
    scla_method = getparm('scla_method')[0][0]
    scla_deramp = getparm('scla_deramp')[0][0]
    subtr_tropo = getparm('subtr_tropo')[0][0]
    tropo_method = getparm('tropo_method')[0][0]

    if use_small_baselines != 0:
        if small_baseline_flag != 'y':
            print('   Use small baselines requested but there are none')
            sys.exit()

    if use_small_baselines == 0:
        # TODO: Implement getparm() function
        scla_drop_index = []  # getparm('scla_drop_index',1);
    else:
        # TODO: if SBaS processing
        # TODO: Implement getparm() function
        scla_drop_index = []  # getparm('sb_scla_drop_index',1);
        print('   Using small baseline interferograms\n')

    psver = loadmat('psver.mat')['psver'][0][0]
    psname = 'ps' + str(psver)
    rcname = 'rc' + str(psver)
    pmname = 'pm' + str(psver)
    bpname = 'bp' + str(psver)
    meanvname = 'mv' + str(psver)
    ifgstdname = 'ifgstd' + str(psver)
    phuwsbresname = 'phuw_sb_res' + str(psver)
    if use_small_baselines == 0:
        phuwname = 'phuw' + str(psver)
        sclaname = 'scla' + str(psver)
        apsname_old = 'aps' + str(psver)  # renamed to old
        apsname = 'tca' + str(psver)  # the new tca option
    else:
        # TODO: if SBaS processing
        phuwname = 'phuw_sb' + str(psver)
        sclaname = 'scla_sb' + str(psver)
        apsname_old = 'aps_sb' + str(psver)  # renamed to old
        apsname = 'tca_sb' + str(psver)  # the new tca option

    if use_small_baselines == 0:
        os.system('rm -f ' + meanvname + '.mat')

    ps = loadmat(psname + '.mat')
    bp = {}
    if os.path.exists(bpname + '.mat'):
        bp = loadmat(bpname + '.mat')
    else:
        bperp = ps['bperp']
        if small_baseline_flag != 'y':
            bperp = np.concatenate((bperp[:ps['master_ix'][0][0] - 1], bperp[ps['master_ix'][0][0]:]), axis=0)
        bp['bperp_mat'] = np.tile(bperp.T, (ps['n_ps'][0][0], 1))
    uw = loadmat(phuwname);

    if small_baseline_flag == 'y' and use_small_baselines == 0:
        # TODO: if SBaS processing
        unwrap_ifg_index = np.arange(0, ps['n_image'][0][0])
        n_ifg = ps['n_image'][0][0]
    else:
        unwrap_ifg_index = np.setdiff1d(np.arange(0, ps['n_ifg'][0][0]), drop_ifg_index)
        n_ifg = ps['n_ifg'][0][0]

    # TODO: subtr_tropo
    # if strcmpi(subtr_tropo,'y')
    # Remove the tropo correction - TRAIN support
    # recompute the APS inversion on the fly as user migth have dropped
    # SB ifgs before and needs new update of the SM APS too.

    # if exist(apsname,'file')~=2
    # the tca file does not exist. See in case this is SM if it needs
    # to be inverted
    #    if strcmpi(apsname,['./tca',num2str(psver)])
    #        if strcmpi(getparm('small_baseline_flag'),'y')
    #           sb_invert_aps(tropo_method)
    #        end
    #     end
    #    aps = load(apsname);
    #    [aps_corr,fig_name_tca,tropo_method] = ps_plot_tca(aps,tropo_method);
    #    uw.ph_uw=uw.ph_uw-aps_corr;
    # end
    # end

    if scla_deramp == 'y':
        print('\n   deramping ifgs...\n')

        [ph_all, ph_ramp] = ps_deramp(ps.copy(), uw['ph_uw'].copy(), 1)
        uw['ph_uw'] = np.subtract(uw['ph_uw'], ph_ramp)

        # ph_ramp=zeros(ps.n_ps,n_ifg,'single');
        # G=double([ones(ps.n_ps,1),ps.xy(:,2),ps.xy(:,3)]);
        # for i=1:length(unwrap_ifg_index)
        #   d=uw.ph_uw(:,unwrap_ifg_index(i));
        #   m=G\double(d(:));
        #   ph_this_ramp=G*m;
        #   uw.ph_uw(:,unwrap_ifg_index(i))=uw.ph_uw(:,unwrap_ifg_index(i))-ph_this_ramp; % subtract ramp
        #   ph_ramp(:,unwrap_ifg_index(i))=ph_this_ramp;
        # end

    else:
        ph_ramp = []

    unwrap_ifg_index = np.setdiff1d(unwrap_ifg_index, scla_drop_index);

    # Check with Andy:
    # 1) should this not be placed before the ramp computation.
    # 2) if this is spatial fitlering in time - not compatible with TRAIN
    # if exist([apsname_old,'.mat'],'file')
    #   if strcmpi(subtr_tropo,'y')
    #       fprintf(['You are removing atmosphere twice. Do not do this, either do:\n use ' apsname_old ' with subtr_tropo=''n''\n remove ' apsname_old ' use subtr_tropo=''y''\n'])
    #   end
    #   aps=load(apsname_old);
    #   uw.ph_uw=uw.ph_uw-aps.ph_aps_slave;
    # end

    ref_ps = ps_setref();

    sys.exit()

"""
Matlab Index
-------------

This is intended for user of SC package to get a close to one-to-one translation to pySC.
Yet, there are differences between Matlab and Python, which have to be resolved on the user side.
The functions are named identically to SC, and they call their pySC equivalents often with different signatures.

"""

from typing import Tuple

import numpy as np
from at import Lattice
from numpy import ndarray

from pySC.core.beam import SCgetBPMreading as bpm_reading, SCgenBunches as generate_bunches
from pySC.core.beam import SCgetBeamTransmission as beam_transmission
from pySC.core.classes import SimulatedComissioning
from pySC.core.lattice_setting import SCsetCavs2SetPoints as cavity_setpoints, SCsetMags2SetPoints as magnet_setpoints, \
    SCsetCMs2SetPoints as cm_setpoints, SCsetMultipoles as multipole_setpoints, SCgetCMSetPoints as get_cm_setpoints, \
    SCcronoff as cronoff
from pySC.correction.injection_fit import SCfitInjectionZ as fit_injection
from pySC.correction.loco_lib import SClocoLib as loco_lib
from pySC.correction.orbit_trajectory import SCfeedbackFirstTurn as first_turn, SCfeedbackStitch as stitch, \
    SCfeedbackRun as frun, SCfeedbackBalance as fbalance, SCpseudoBBA as pseudo_bba
from pySC.correction.ramp_errors import SCrampUpErrors as ramp_up_errors
from pySC.correction.rf import SCsynchPhaseCorrection as synch_phase_corr, SCsynchEnergyCorrection as synch_energy_corr
from pySC.correction.tune import SCtuneScan as tune_scan
from pySC.lattice_properties.apertures import SCdynamicAperture as dynamic_aperture, \
    SCmomentumAperture as momentum_aperture
# from pySC.correction.bba import SCBBA as bba
from pySC.lattice_properties.magnet_orbit import SCgetCOD as cod
from pySC.lattice_properties.response_measurement import SCgetRespMat as response_matrix, SCgetDispersion as dispersion
from pySC.lattice_properties.response_model import SCgetModelRM as model_rm, SCgetModelDispersion as model_dispersion, \
    SCgetModelRING as model_ring
from pySC.plotting.SCplotCMstrengths import SCplotCMstrengths as plot_cm_strength
from pySC.plotting.SCplotLattice import SCplotLattice as plot_lattice
from pySC.plotting.SCplotPhaseSpace import SCplotPhaseSpace as plot_phase_space
from pySC.plotting.SCplotSupport import SCplotSupport as plot_support
from pySC.utils import logging_tools
from pySC.utils.sc_tools import SCgetOrds as get_ords, SCgetPinv as get_pinv, SCrandnc as randnc, \
    SCscaleCircumference as scale_circumference, SCgetTransformation as transform, SCmultipolesRead as read_multipoles

LOGGER = logging_tools.get_logger(__name__)
LOGGER.warn("Matlab_index imported: \n"
            "             This module is intended only to aid translation between SC and pySC.\n"
            "             For any important use cases, please consider using pySC methods directly.\n")


def SCapplyErrors(SC: SimulatedComissioning, nsigmas: float = 2) -> SimulatedComissioning:
    SC.apply_errors(nsigmas=nsigmas)
    return SC


def SCBBA(SC, BPMords, magOrds, **kwargs):
    return NotImplementedError
    return bba(SC, BPMords, magOrds, **kwargs)


def SCcronoff(ring: Lattice, *args: str) -> Lattice:
    return cronoff(ring, *args)


def SCdynamicAperture(RING, dE, /, *, bounds=np.array([0, 1e-3]), nturns=1000, thetas=np.linspace(0, 2 * np.pi, 16),
                      accuracy=1e-6, launchOnOrbit=False, centerOnOrbit=True, useOrbit6=False, auto=0, plot=False,
                      verbose=False):
    return dynamic_aperture(RING, dE, bounds=bounds, nturns=nturns, thetas=thetas, accuracy=accuracy,
                            launchOnOrbit=launchOnOrbit, centerOnOrbit=centerOnOrbit, useOrbit6=useOrbit6, auto=auto,
                            plot=plot)


def SCfeedbackBalance(SC, Mplus, /, *, R0=None, CMords=None, BPMords=None, eps=1e-4, maxsteps=10, verbose=False):
    return fbalance(SC, Mplus, reference=R0, CMords=CMords, BPMords=BPMords, eps=eps, maxsteps=maxsteps)


def SCfeedbackFirstTurn(SC, Mplus, /, *, R0=None, CMords=None, BPMords=None, maxsteps=100, wiggleAfter=20,
                        wiggleSteps=32, wiggleRange=np.array([500E-6, 1000E-6]), verbose=False):
    return first_turn(SC, Mplus, reference=R0, CMords=CMords, BPMords=BPMords, maxsteps=maxsteps,
                      wiggle_after=wiggleAfter,
                      wiggle_steps=wiggleSteps, wiggle_range=wiggleRange)


def SCfeedbackRun(SC, Mplus, /, *, R0=None, CMords=None, BPMords=None, eps=1e-4, target=0, maxsteps=30, scaleDisp=0,
                  weight=None, verbose=False):
    return frun(SC, Mplus, reference=R0, CMords=CMords, BPMords=BPMords, eps=eps, target=target, maxsteps=maxsteps,
                scaleDisp=scaleDisp)


def SCfeedbackStitch(SC, Mplus, /, *, R0=None, CMords=None, BPMords=None, nBPMs=4, maxsteps=30, nRepro=3,
                     wiggle_steps=32,
                     wiggle_range=np.array([500E-6, 1000E-6])):
    return stitch(SC, Mplus, reference=R0, CMords=CMords, BPMords=BPMords, nBPMs=nBPMs, maxsteps=maxsteps,
                  nRepro=nRepro,
                  wiggle_steps=wiggle_steps, wiggle_range=wiggle_range)


def SCfitInjectionZ(SC, mode, /, *, nDims=np.array([0, 1]), nBPMs=np.array([0, 1, 2]), nShots=None, verbose=0,
                    plotFlag=False):
    return fit_injection(SC, mode, nDims=nDims, nBPMs=nBPMs, nShots=nShots, plotFlag=plotFlag)


def SCgenBunches(SC: SimulatedComissioning) -> ndarray:
    return generate_bunches(SC)


def SCgetBeamTransmission(SC: SimulatedComissioning, /, *, nParticles: int = None, nTurns: int = None,
                          plotFlag: bool = False, verbose: bool = False) -> Tuple[int, ndarray]:
    return beam_transmission(SC, nParticles, nTurns=nTurns, do_plot=plotFlag)


def SCgetBPMreading(SC, /, *, BPMords=None):
    return bpm_reading(SC, BPMords=BPMords)


def SCgetCMSetPoints(SC: SimulatedComissioning, CMords: ndarray, nDim: int) -> ndarray:
    LOGGER.warn("Function SCgetCMSetPoints contains non-trivial transition between Matlab and Python code.\n"
                "Transition concerns nDim 1 -> horizontal, 2-> vertical.")
    if nDim not in (1, 2):
        raise ValueError("Function expects nDim 1 (hor) or 2 (ver)")
    return get_cm_setpoints(SC, CMords=CMords, skewness=(nDim == 2))


def SCgetCOD(SC, /, *, ords=None, plot=False):
    return cod(SC, ords=ords, plot=plot)


def SCgetDispersion(SC, RFstep, /, *, BPMords=None, CAVords=None, nSteps=2):
    return dispersion(SC, RFstep, BPMords=BPMords, CAVords=CAVords, nSteps=nSteps)


def SCgetModelDispersion(SC, BPMords, CAVords, /, *, trackMode='ORB', Z0=np.zeros(6), nTurns=1, rfStep=1E3,
                         useIdealRing=True):
    return model_dispersion(SC, BPMords, CAVords, trackMode=trackMode, Z0=Z0, nTurns=nTurns, rfStep=rfStep,
                            useIdealRing=useIdealRing)


def SCgetModelRING(SC: SimulatedComissioning, /, *, includeAperture: bool = False) -> Lattice:
    return model_ring(SC, includeAperture=includeAperture)


def SCgetModelRM(SC, BPMords, CMords, /, *, trackMode='TBT', Z0=np.zeros(6), nTurns=1, dkick=1e-5, useIdealRing=True):
    return model_rm(SC, BPMords=BPMords, CMords=CMords, trackMode=trackMode, Z0=Z0, nTurns=nTurns, dkick=dkick,
                    useIdealRing=useIdealRing)


def SCgetOrds(ring: Lattice, regex: str, /, *, verbose: bool = False) -> ndarray:
    return get_ords(ring=ring, regex=regex)


def SCgetPinv(matrix: ndarray, /, *, N: int = 0, alpha: float = 0, damping: float = 1, plot: bool = False) -> ndarray:
    return get_pinv(matrix=matrix, num_removed=N, alpha=alpha, damping=damping, plot=plot)


def SCgetRespMat(SC, Amp, BPMords, CMords, /, *, mode='fixedKick', nSteps=2, fit='linear', verbose=0):
    return response_matrix(SC, Amp, BPMords, CMords, mode=mode, nSteps=nSteps, fit=fit)


def SCgetSupportOffset(SC: SimulatedComissioning, s: ndarray) -> ndarray:
    offsets, rolls = SC.support_offset_and_roll(s)
    return offsets


def SCgetSupportRoll(SC: SimulatedComissioning, s: ndarray) -> ndarray:
    offsets, rolls = SC.support_offset_and_roll(s)
    return rolls


def SCgetTransformation(dx, dy, dz, ax, ay, az, magTheta, magLength, refPoint='center'):
    return transform(np.array([dx, dy, dz]), np.array([ax, ay, az]), magTheta, magLength, refPoint=refPoint)


def SCinit(RING: Lattice) -> SimulatedComissioning:
    return SimulatedComissioning(RING)


def SClocoLib(funName, *args):
    return loco_lib(funName, *args)


def SCmomentumAperture(RING, REFPTS, inibounds, /, *, nturns=1000, accuracy=1e-4, stepsize=1e-3, plot=0, debug=0):
    return momentum_aperture(RING, REFPTS, inibounds, nturns=nturns, accuracy=accuracy, stepsize=stepsize, plot=plot)


def SCmultipolesRead(fname):
    return read_multipoles(fname)


def SCparticlesIn3D(*args):
    raise NotImplementedError("No longer needed")


def SCplotBPMreading(SC, B=None, T=None):
    init_plot = SC.plot
    SC.plot = True
    bpm_reading(SC)
    SC.plot = init_plot
    return SC


def SCplotCMstrengths(SC: SimulatedComissioning):
    plot_cm_strength(SC)


def SCplotLattice(SC, /, *, transferLine=0, nSectors=1, oList=[], plotIdealRing=1, sRange=[], plotMagNames=0,
                  fontSize=16):
    return plot_lattice(SC, transferLine=transferLine, nSectors=nSectors, oList=oList, plotIdealRing=plotIdealRing,
                        sRange=sRange, plotMagNames=plotMagNames, fontSize=fontSize)


def SCplotPhaseSpace(SC, /, *, ord=np.zeros(1), customBunch=[], nParticles=None, nTurns=None, plotCO=False):
    plot_phase_space(SC, ord=ord, customBunch=customBunch, nParticles=nParticles, nTurns=nTurns, plotCO=plotCO)


def SCplotSupport(SC: SimulatedComissioning, /, *, fontSize: int = 8, xLim: Tuple[float, float] = None, ShiftAxes=None):
    plot_support(SC, fontSize=fontSize, xLim=xLim)


def SCpseudoBBA(SC, BPMords, MagOrds, postBBAoffset, /, *, sigma=2):
    return pseudo_bba(SC, BPMords, MagOrds, postBBAoffset, sigma=sigma)


def SCrampUpErrors(SC, /, *, nStepsRamp=10, eps=1e-5, target=0, alpha=10, maxsteps=30, verbose=0):
    return ramp_up_errors(SC, nStepsRamp=nStepsRamp, eps=eps, target=target, alpha=alpha, maxsteps=maxsteps)


def SCrandnc(cut_off: float = 2, shape: tuple = (1,)) -> ndarray:
    return randnc(cut_off, shape)


def SCregisterBPMs(SC: SimulatedComissioning, BPMords: ndarray, **kwargs) -> SimulatedComissioning:
    SC.register_bpms(ords=BPMords, **kwargs)
    return SC


def SCregisterCAVs(SC: SimulatedComissioning, CAVords: ndarray, **kwargs) -> SimulatedComissioning:
    SC.register_cavities(ords=CAVords, **kwargs)
    return SC


def SCregisterMagnets(SC: SimulatedComissioning, MAGords: ndarray, **kwargs) -> SimulatedComissioning:
    SC.register_magnets(ords=MAGords, **kwargs)
    return SC


def SCregisterSupport(SC: SimulatedComissioning, support_type: str, support_ords: ndarray,
                      **kwargs) -> SimulatedComissioning:
    SC.register_supports(support_ords=support_ords, support_type=support_type, **kwargs)
    return SC


def SCSanityCheck(SC: SimulatedComissioning) -> None:
    SC.verify_structure()


def SCscaleCircumference(RING, circ, /, *, mode='abs'):
    return scale_circumference(RING, circ, mode=mode)


def SCsetCavs2SetPoints(SC: SimulatedComissioning, CAVords: ndarray, type: str, setpoints: ndarray, /, *,
                        mode: str = 'abs') -> SimulatedComissioning:
    return cavity_setpoints(SC, CAVords=CAVords, type=type, setpoints=setpoints, method=mode)


def SCsetCMs2SetPoints(SC: SimulatedComissioning, CMords: ndarray, setpoints: ndarray, nDim: int, /, *,
                       mode: str = 'abs') -> Tuple[SimulatedComissioning, ndarray]:
    LOGGER.warn("Function SCsetCM2SetPoints contains non-trivial transition between Matlab and Python code.\n"
                "Transition concerns nDim 1 -> horizontal, 2-> vertical.")
    if nDim not in (1, 2):
        raise ValueError("Function expects nDim 1 (hor) or 2 (ver)")
    return cm_setpoints(SC, CMords=CMords, setpoints=setpoints, skewness=(nDim == 2), method=mode)


def SCsetMags2SetPoints(SC: SimulatedComissioning, MAGords: ndarray, type: int, order: int, setpoints: ndarray, /, *,
                        method: str = 'abs', dipCompensation: bool = False) -> SimulatedComissioning:
    LOGGER.warn("Function SCsetMags2SetPoints contains non-trivial transition between Matlab and Python code.\n"
                "Transition concerns:    type 1 -> skew, 2-> normal. \n"
                "                        order 1 -> dipole, 2-> quadrupole, 3-> sextupole, ...")
    if type not in (1, 2):
        raise ValueError("Function expects type 1 (skew) or 2 (normal)")

    return magnet_setpoints(SC, MAGords=MAGords, skewness=(type == 1), order=order - 1, setpoints=setpoints,
                            method=method, dipCompensation=dipCompensation)


def SCsetMultipoles(RING, ords: ndarray, AB, /, *, method: str = 'rnd', order: int = None, type: int = None):
    LOGGER.warn("Function SCsetMultipoles contains non-trivial transition between Matlab and Python code.\n"
                "Transition concerns:    type 1 -> skew, 2-> normal. \n"
                "                        order 1 -> dipole, 2-> quadrupole, 3-> sextupole, ...\n"
                "                        AB [N x 2] numpy.array of PolynomA and PolynomB")
    if AB.ndim != 2:
        raise ValueError("AB has to be numpy.array of shape N x 2.")
    if type is not None:
        if type not in (1, 2):
            raise ValueError("Function expects type 1 (skew) or 2 (normal)")
    return multipole_setpoints(RING=RING, ords=ords, BA=np.roll(AB, 1, axis=1), method=method,
                               order=None if order is None else order - 1,
                               skewness=None if order is None else (type == 1))


def SCsynchEnergyCorrection(SC, /, *, cavOrd=None, f_range=(-1E3, 1E3), nSteps=15, nTurns=150, minTurns=0,
                            plotResults=False,
                            plotProgress=False, verbose=False):
    init_nturns = SC.INJ.nTurns
    SC.INJ.nTurns = nTurns
    SC = synch_energy_corr(SC, cavOrd=cavOrd, f_range=f_range, nSteps=nSteps, minTurns=minTurns,
                           plotResults=plotResults, plotProgress=plotProgress, )
    SC.INJ.nTurns = init_nturns
    return SC


def SCsynchPhaseCorrection(SC, /, *, cavOrd=None, nSteps=15, nTurns=20, plotResults=False, plotProgress=False,
                           verbose=False):
    init_nturns = SC.INJ.nTurns
    SC.INJ.nTurns = nTurns
    SC = synch_phase_corr(SC, cavOrd=cavOrd, nSteps=nSteps, plotResults=plotResults, plotProgress=plotProgress, )
    SC.INJ.nTurns = init_nturns
    return SC


def SCtuneScan(SC, qOrds, qSPvec, /, *, verbose=False, plotFlag=False, nParticles=None, nTurns=None, target=1,
               fullScan=0):
    return tune_scan(SC, qOrds, qSPvec, plotFlag=plotFlag, nParticles=nParticles, nTurns=nTurns,
                     target=target, fullScan=fullScan)


def SCupdateCAVs(SC: SimulatedComissioning, ords: ndarray = None) -> SimulatedComissioning:
    SC.update_cavities(ords=ords)
    return SC


def SCupdateMagnets(SC: SimulatedComissioning, ords: ndarray = None) -> SimulatedComissioning:
    SC.update_magnets(ords=ords)
    return SC


def SCupdateSupport(SC: SimulatedComissioning, BPMstructOffset: bool = True,
                    MAGstructOffset: bool = True) -> SimulatedComissioning:
    SC.update_supports(offset_bpms=BPMstructOffset, offset_magnets=MAGstructOffset)
    return SC
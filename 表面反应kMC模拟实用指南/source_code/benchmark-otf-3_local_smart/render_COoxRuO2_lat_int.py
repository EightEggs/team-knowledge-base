#!/usr/bin/env python

"""
Renders and builds a kmos model for CO oxidation on RuO2.
It can render models for the different backends and
adds a given amount of lateral interactions automatically.
"""

from itertools import product
import os
import sys
import time

import numpy as np

from kmcos.cli import main as cli_main
from kmcos.types import (
    Action,
    Bystander,
    Condition,
    Layer,
    Process,
    Project,
    Site,
    Species,
)


def render_model(lat_ints, backend, compile_time_path=None):
    """
    Parameters:
    -----------
    lat_ints : int
        amount of bystanders for each process
    backend : str
        kmos backend in ('otf', 'local_smart', 'lat_int')
    compile_time_path : str
        If it is not None, store the compile time
        in a file using the .csv format
    """

    # Project
    pt = Project()
    pt.set_meta(
        author="Michael Seibt",
        email="michael.seibt@tum.de",
        model_name="benchmark-{backend}-{lat_ints}".format(
            backend=backend, lat_ints=lat_ints
        ),
        model_dimension=2,
    )

    # Species
    pt.add_species(
        Species(name="empty", color="#ffffff"),
        Species(
            name="CO", color="#000000", representation="Atoms('CO',[[0,0,0],[0,0,1.2]])"
        ),
        Species(name="O", color="#ff0000", representation="Atoms('O')"),
    )
    pt.species_list.default_species = "empty"

    # Lattice
    layer = Layer(name="ruo2")
    layer.add_site(
        Site(name="bridge", pos="0.0 0.5 0.7"), Site(name="cus", pos="0.5 0.5 0.7")
    )
    pt.add_layer(layer)

    pt.lattice.representation = """[
    Atoms(symbols='O2Ru2',
          pbc=np.array([False, False, False], dtype=bool),
          cell=np.array(
        [[ 6.39 ,   0.   ,   0.   ],
        [  0.   ,   3.116,   0.   ],
        [  0.   ,   0.   ,  20.   ]]),
          positions=np.array(
        [[ 4.435981  ,   0.        ,  10. ],
        [  1.95416379,   0.        ,  10. ],
        [  0.        ,   0.        ,  10. ],
        [  3.1950724 ,   1.5582457 ,  10. ]]))
    ]"""
    pt.lattice.cell = np.diag([6.43, 3.12, 20])

    # Coordinates
    cus = pt.lattice.generate_coord("cus.(0,0,0).ruo2")
    cus_right = pt.lattice.generate_coord("bridge.(1,0,0).ruo2")
    cus_up = pt.lattice.generate_coord("cus.(0,1,0).ruo2")

    bridge = pt.lattice.generate_coord("bridge.(0,0,0).ruo2")
    bridge_right = pt.lattice.generate_coord("cus.(0,0,0).ruo2")
    bridge_up = pt.lattice.generate_coord("bridge.(0,1,0).ruo2")

    # Bystander coordinates
    base_bystander_list = pt.lattice.generate_coord_set(
        size=[2, 2, 1], layer_name="ruo2"
    )

    cus_ads_nn = [
        coord
        for coord in base_bystander_list
        if coord
        not in [
            cus,
        ]
    ][:lat_ints]
    bri_ads_nn = [
        coord
        for coord in base_bystander_list
        if coord
        not in [
            bridge,
        ]
    ][:lat_ints]
    cus_up_nn = [coord for coord in base_bystander_list if coord not in [cus, cus_up]][
        :lat_ints
    ]
    bri_up_nn = [
        coord for coord in base_bystander_list if coord not in [bridge, bridge_up]
    ][:lat_ints]
    bri_cus_nn = [
        coord for coord in base_bystander_list if coord not in [bridge, bridge_right]
    ][:lat_ints]
    cus_bri_nn = [
        coord for coord in base_bystander_list if coord not in [cus, cus_right]
    ][:lat_ints]

    # Bystanders
    allowed_species = ["O", "CO"]
    cus_ads_bystanders = [
        Bystander(coord=coord, allowed_species=allowed_species, flag="1nn")
        for coord in cus_ads_nn
    ]
    bri_ads_bystanders = [
        Bystander(coord=coord, allowed_species=allowed_species, flag="1nn")
        for coord in bri_ads_nn
    ]
    cus_up_bystanders = [
        Bystander(coord=coord, allowed_species=allowed_species, flag="1nn")
        for coord in cus_up_nn
    ]
    bri_up_bystanders = [
        Bystander(coord=coord, allowed_species=allowed_species, flag="1nn")
        for coord in bri_up_nn
    ]
    bri_cus_bystanders = [
        Bystander(coord=coord, allowed_species=allowed_species, flag="1nn")
        for coord in bri_cus_nn
    ]
    cus_bri_bystanders = [
        Bystander(coord=coord, allowed_species=allowed_species, flag="1nn")
        for coord in cus_bri_nn
    ]

    # Parameters
    pt.add_parameter(
        name="p_COgas", value=1e-10, adjustable=True, min=1e-13, max=1e2, scale="log"
    )
    pt.add_parameter(
        name="p_O2gas", value=1e-5, adjustable=True, min=1e-15, max=1e2, scale="log"
    )
    pt.add_parameter(name="T", value=350, adjustable=True, min=300, max=1500)

    pt.add_parameter(
        name="A",
        value="%s*angstrom**2" % (pt.lattice.cell[0, 0] * pt.lattice.cell[1, 1]),
    )
    pt.add_parameter(name="E_O_bridge", value=-2.3)
    pt.add_parameter(name="E_O_cus", value=-1.0)
    pt.add_parameter(name="E_CO_bridge", value=-1.6)
    pt.add_parameter(name="E_CO_cus", value=-1.3)

    pt.add_parameter(name="E_react_Ocus_COcus", value=0.9)
    pt.add_parameter(name="E_react_Ocus_CObridge", value=0.8)
    pt.add_parameter(name="E_react_Obridge_COcus", value=1.2)
    pt.add_parameter(name="E_react_Obridge_CObridge", value=1.5)

    pt.add_parameter(name="E_COdiff_cus_cus", value=1.7)
    pt.add_parameter(name="E_COdiff_cus_bridge", value=1.3)
    pt.add_parameter(name="E_COdiff_bridge_bridge", value=0.6)
    pt.add_parameter(name="E_COdiff_bridge_cus", value=1.6)

    pt.add_parameter(name="E_Odiff_cus_cus", value=1.6)
    pt.add_parameter(name="E_Odiff_bridge_bridge", value=0.7)
    pt.add_parameter(name="E_Odiff_bridge_cus", value=2.3)
    pt.add_parameter(name="E_Odiff_cus_bridge", value=1.0)

    class ProcessHolder(object):
        """
        Serves as a container for processes to manipulate these
        processes on the fly according to the backend used for compilation.
        I.e. add processes for all configurations and don't add *bystander_list*
        and *otf_rate* for the local_smart and lat_int backend.
        """

        def __init__(self):
            """basic processes"""
            self.processes = []
            self.process_counter = 0

        def add_process(self, **kwargs):
            """add basic process to this holder"""
            self.processes.append(kwargs)

        def add_project_processes(self, pt, backend="otf"):
            """add all processes to the project according to the backend"""
            if backend == "otf":
                for process in self.processes:
                    pt.add_process(**process)
            elif backend == "local_smart" or backend == "lat_int":
                # iterate over forward and backward processes together, to group them manually for
                # the acceleration algorithm
                for forward_process, backward_process in zip(
                    self.processes[0::2], self.processes[1::2]
                ):
                    forward_process.pop("otf_rate")
                    backward_process.pop("otf_rate")

                    # bystanders are the same for both processes here
                    backward_process.pop("bystander_list")
                    coords = [c.coord for c in forward_process.pop("bystander_list")]

                    # naming of actions
                    forward_process["action_list"] = forward_process.pop("actions")
                    backward_process["action_list"] = backward_process.pop("actions")

                    forward_base_conditions = forward_process.pop("conditions")
                    backward_base_conditions = backward_process.pop("conditions")

                    forward_name = forward_process.pop("name")
                    backward_name = backward_process.pop("name")

                    # bystanders are represented as additional processes with more conditions
                    # for each species configuration add an process
                    for conf in product(["empty", "O", "CO"], repeat=lat_ints):
                        forward_process["name"] = "{name}_{count}".format(
                            name=forward_name, count=self.process_counter
                        )
                        backward_process["name"] = "{name}_{count}".format(
                            name=backward_name, count=self.process_counter
                        )
                        forward_process["paired_with"] = str(self.process_counter)
                        backward_process["paired_with"] = str(self.process_counter)

                        forward_process["condition_list"] = forward_base_conditions[:]
                        backward_process["condition_list"] = backward_base_conditions[:]

                        # add a condition for each observed bystander site
                        # given the current species configuration
                        for tmp_species, tmp_coord in zip(conf, coords):
                            forward_process["condition_list"].append(
                                Condition(species=tmp_species, coord=tmp_coord)
                            )
                            backward_process["condition_list"].append(
                                Condition(species=tmp_species, coord=tmp_coord)
                            )

                        pt.add_process(Process(**forward_process))
                        pt.add_process(Process(**backward_process))

                        self.process_counter += 1
            return pt

    process_holder = ProcessHolder()

    # Processes
    # CO Adsorption/Desorption
    process_holder.add_process(
        name="CO_adsorption_cus",
        conditions=[Condition(species="empty", coord=cus)],
        actions=[Action(species="CO", coord=cus)],
        bystander_list=cus_ads_bystanders,
        rate_constant="p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )
    process_holder.add_process(
        name="CO_desorption_cus",
        conditions=[Condition(species="CO", coord=cus)],
        actions=[Action(species="empty", coord=cus)],
        bystander_list=cus_ads_bystanders,
        rate_constant="p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)*exp(beta*(E_CO_cus-mu_COgas)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )

    process_holder.add_process(
        name="CO_adsorption_bridge",
        conditions=[Condition(species="empty", coord=bridge)],
        actions=[Action(species="CO", coord=bridge)],
        bystander_list=bri_ads_bystanders,
        rate_constant="p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )
    process_holder.add_process(
        name="CO_desorption_bridge",
        conditions=[Condition(species="CO", coord=bridge)],
        actions=[Action(species="empty", coord=bridge)],
        bystander_list=bri_ads_bystanders,
        rate_constant="p_COgas*bar*A/2/sqrt(2*pi*umass*m_CO/beta)*exp(beta*(E_CO_bridge-mu_COgas)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )

    # CO diffusion
    # cus/cus
    process_holder.add_process(
        name="COdiff_cus_up",
        conditions=[
            Condition(species="CO", coord=cus),
            Condition(species="empty", coord=cus_up),
        ],
        actions=[
            Condition(species="empty", coord=cus),
            Condition(species="CO", coord=cus_up),
        ],
        bystander_list=cus_up_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*(E_COdiff_cus_cus)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )
    process_holder.add_process(
        name="COdiff_cus_down",
        conditions=[
            Condition(species="CO", coord=cus_up),
            Condition(species="empty", coord=cus),
        ],
        actions=[
            Condition(species="empty", coord=cus_up),
            Condition(species="CO", coord=cus),
        ],
        bystander_list=cus_up_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*(E_COdiff_cus_cus)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )

    # bridge/bridge
    process_holder.add_process(
        name="COdiff_bridge_up",
        conditions=[
            Condition(species="CO", coord=bridge),
            Condition(species="empty", coord=bridge_up),
        ],
        actions=[
            Condition(species="empty", coord=bridge),
            Condition(species="CO", coord=bridge_up),
        ],
        bystander_list=bri_up_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*(E_COdiff_bridge_bridge)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )
    process_holder.add_process(
        name="COdiff_bridge_down",
        conditions=[
            Condition(species="CO", coord=bridge_up),
            Condition(species="empty", coord=bridge),
        ],
        actions=[
            Condition(species="empty", coord=bridge_up),
            Condition(species="CO", coord=bridge),
        ],
        bystander_list=bri_up_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*(E_COdiff_bridge_bridge)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )

    # bridge/cus
    process_holder.add_process(
        name="COdiff_bridge_right",
        conditions=[
            Condition(species="CO", coord=bridge),
            Condition(species="empty", coord=bridge_right),
        ],
        actions=[
            Condition(species="empty", coord=bridge),
            Condition(species="CO", coord=bridge_right),
        ],
        bystander_list=bri_cus_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*(E_COdiff_bridge_cus)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )
    process_holder.add_process(
        name="COdiff_bridge_left",
        conditions=[
            Condition(species="CO", coord=bridge_right),
            Condition(species="empty", coord=bridge),
        ],
        actions=[
            Condition(species="empty", coord=bridge_right),
            Condition(species="CO", coord=bridge),
        ],
        bystander_list=bri_cus_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*(E_COdiff_cus_bridge)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )

    # bridge/cus
    process_holder.add_process(
        name="COdiff_cus_right",
        conditions=[
            Condition(species="CO", coord=cus),
            Condition(species="empty", coord=cus_right),
        ],
        actions=[
            Condition(species="empty", coord=cus),
            Condition(species="CO", coord=cus_right),
        ],
        bystander_list=cus_bri_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*(E_COdiff_cus_bridge)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )
    process_holder.add_process(
        name="COdiff_cus_left",
        conditions=[
            Condition(species="CO", coord=cus_right),
            Condition(species="empty", coord=cus),
        ],
        actions=[
            Condition(species="empty", coord=cus_right),
            Condition(species="CO", coord=cus),
        ],
        bystander_list=cus_bri_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*(E_COdiff_bridge_cus)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )

    # O2 Adsorption/Desorption
    # avoiding double-counting ...
    process_holder.add_process(
        name="O2_adsorption_cus_up",
        conditions=[
            Condition(species="empty", coord=cus),
            Condition(species="empty", coord=cus_up),
        ],
        actions=[
            Condition(species="O", coord=cus),
            Condition(species="O", coord=cus_up),
        ],
        bystander_list=cus_up_bystanders,
        rate_constant="p_O2gas*bar*A/sqrt(2*pi*umass*m_O2/beta)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )
    process_holder.add_process(
        name="O2_desorption_cus_up",
        conditions=[
            Condition(species="O", coord=cus),
            Condition(species="O", coord=cus_up),
        ],
        actions=[
            Condition(species="empty", coord=cus),
            Condition(species="empty", coord=cus_up),
        ],
        bystander_list=cus_up_bystanders,
        rate_constant="p_O2gas*bar*A/sqrt(2*pi*umass*m_O2/beta)*exp(beta*(2*E_O_cus-mu_O2gas)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )

    process_holder.add_process(
        name="O2_adsorption_cus_right",
        conditions=[
            Condition(species="empty", coord=cus),
            Condition(species="empty", coord=cus_right),
        ],
        actions=[
            Condition(species="O", coord=cus),
            Condition(species="O", coord=cus_right),
        ],
        bystander_list=cus_bri_bystanders,
        rate_constant="p_O2gas*bar*A/sqrt(2*pi*umass*m_O2/beta)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )
    process_holder.add_process(
        name="O2_desorption_cus_right",
        conditions=[
            Condition(species="O", coord=cus),
            Condition(species="O", coord=cus_right),
        ],
        actions=[
            Condition(species="empty", coord=cus),
            Condition(species="empty", coord=cus_right),
        ],
        bystander_list=cus_bri_bystanders,
        rate_constant="p_O2gas*bar*A/sqrt(2*pi*umass*m_O2/beta)*exp(beta*((E_O_cus+E_O_bridge)-mu_O2gas)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )

    process_holder.add_process(
        name="O2_adsorption_bridge_up",
        conditions=[
            Condition(species="empty", coord=bridge),
            Condition(species="empty", coord=bridge_up),
        ],
        actions=[
            Condition(species="O", coord=bridge),
            Condition(species="O", coord=bridge_up),
        ],
        bystander_list=bri_up_bystanders,
        rate_constant="p_O2gas*bar*A/sqrt(2*pi*umass*m_O2/beta)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )
    process_holder.add_process(
        name="O2_desorption_bridge_up",
        conditions=[
            Condition(species="O", coord=bridge),
            Condition(species="O", coord=bridge_up),
        ],
        actions=[
            Condition(species="empty", coord=bridge),
            Condition(species="empty", coord=bridge_up),
        ],
        bystander_list=bri_up_bystanders,
        rate_constant="p_O2gas*bar*A/sqrt(2*pi*umass*m_O2/beta)*exp(beta*(2*E_O_bridge-mu_O2gas)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )

    process_holder.add_process(
        name="O2_adsorption_bridge_right",
        conditions=[
            Condition(species="empty", coord=bridge),
            Condition(species="empty", coord=bridge_right),
        ],
        actions=[
            Condition(species="O", coord=bridge),
            Condition(species="O", coord=bridge_right),
        ],
        bystander_list=bri_cus_bystanders,
        rate_constant="p_O2gas*bar*A/sqrt(2*pi*umass*m_O2/beta)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )
    process_holder.add_process(
        name="O2_desorption_bridge_right",
        conditions=[
            Condition(species="O", coord=bridge),
            Condition(species="O", coord=bridge_right),
        ],
        actions=[
            Condition(species="empty", coord=bridge),
            Condition(species="empty", coord=bridge_right),
        ],
        bystander_list=bri_cus_bystanders,
        rate_constant="p_O2gas*bar*A/sqrt(2*pi*umass*m_O2/beta)*exp(beta*((E_O_bridge+E_O_cus)-mu_O2gas)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )

    # O diffusion
    # cus/cus
    process_holder.add_process(
        name="Odiff_cus_up",
        conditions=[
            Condition(species="O", coord=cus),
            Condition(species="empty", coord=cus_up),
        ],
        actions=[
            Condition(species="empty", coord=cus),
            Condition(species="O", coord=cus_up),
        ],
        bystander_list=cus_up_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*(E_Odiff_cus_cus)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )
    process_holder.add_process(
        name="Odiff_cus_down",
        conditions=[
            Condition(species="O", coord=cus_up),
            Condition(species="empty", coord=cus),
        ],
        actions=[
            Condition(species="empty", coord=cus_up),
            Condition(species="O", coord=cus),
        ],
        bystander_list=cus_up_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*(E_Odiff_cus_cus)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )

    # bridge/bridge
    process_holder.add_process(
        name="Odiff_bridge_up",
        conditions=[
            Condition(species="O", coord=bridge),
            Condition(species="empty", coord=bridge_up),
        ],
        actions=[
            Condition(species="empty", coord=bridge),
            Condition(species="O", coord=bridge_up),
        ],
        bystander_list=bri_up_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*(E_Odiff_bridge_bridge)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )
    process_holder.add_process(
        name="Odiff_bridge_down",
        conditions=[
            Condition(species="O", coord=bridge_up),
            Condition(species="empty", coord=bridge),
        ],
        actions=[
            Condition(species="empty", coord=bridge_up),
            Condition(species="O", coord=bridge),
        ],
        bystander_list=bri_up_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*(E_Odiff_bridge_bridge)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )

    # bridge/cus
    process_holder.add_process(
        name="Odiff_bridge_right",
        conditions=[
            Condition(species="O", coord=bridge),
            Condition(species="empty", coord=bridge_right),
        ],
        actions=[
            Condition(species="empty", coord=bridge),
            Condition(species="O", coord=bridge_right),
        ],
        bystander_list=bri_cus_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*(E_Odiff_bridge_cus)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )
    process_holder.add_process(
        name="Odiff_bridge_left",
        conditions=[
            Condition(species="O", coord=bridge_right),
            Condition(species="empty", coord=bridge),
        ],
        actions=[
            Condition(species="empty", coord=bridge_right),
            Condition(species="O", coord=bridge),
        ],
        bystander_list=bri_cus_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*(E_Odiff_cus_bridge)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )

    # bridge/cus
    process_holder.add_process(
        name="Odiff_cus_right",
        conditions=[
            Condition(species="O", coord=cus),
            Condition(species="empty", coord=cus_right),
        ],
        actions=[
            Condition(species="empty", coord=cus),
            Condition(species="O", coord=cus_right),
        ],
        bystander_list=cus_bri_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*(E_Odiff_cus_bridge)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )
    process_holder.add_process(
        name="Odiff_cus_left",
        conditions=[
            Condition(species="O", coord=cus_right),
            Condition(species="empty", coord=cus),
        ],
        actions=[
            Condition(species="empty", coord=cus_right),
            Condition(species="O", coord=cus),
        ],
        bystander_list=cus_bri_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*(E_Odiff_bridge_cus)*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
    )

    # Reaction
    process_holder.add_process(
        name="React_cus_up",
        conditions=[
            Condition(species="O", coord=cus),
            Condition(species="CO", coord=cus_up),
        ],
        actions=[
            Action(species="empty", coord=cus),
            Action(species="empty", coord=cus_up),
        ],
        bystander_list=cus_up_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*E_react_Ocus_COcus*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
        tof_count={"CO_oxidation": 1},
    )
    process_holder.add_process(
        name="Ads_cus_up",
        conditions=[
            Condition(species="empty", coord=cus),
            Condition(species="empty", coord=cus_up),
        ],
        actions=[Action(species="O", coord=cus), Action(species="CO", coord=cus_up)],
        bystander_list=cus_up_bystanders,
        rate_constant="0",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
        tof_count={"CO_oxidation": -1},
    )

    process_holder.add_process(
        name="React_cus_down",
        conditions=[
            Condition(species="O", coord=cus_up),
            Condition(species="CO", coord=cus),
        ],
        actions=[
            Action(species="empty", coord=cus_up),
            Action(species="empty", coord=cus),
        ],
        bystander_list=cus_up_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*E_react_Ocus_COcus*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
        tof_count={"CO_oxidation": 1},
    )
    process_holder.add_process(
        name="Ads_cus_down",
        conditions=[
            Condition(species="empty", coord=cus_up),
            Condition(species="empty", coord=cus),
        ],
        actions=[Action(species="O", coord=cus_up), Action(species="CO", coord=cus)],
        bystander_list=cus_up_bystanders,
        rate_constant="0",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
        tof_count={"CO_oxidation": -1},
    )

    process_holder.add_process(
        name="React_cus_right",
        conditions=[
            Condition(species="O", coord=cus),
            Condition(species="CO", coord=cus_right),
        ],
        actions=[
            Action(species="empty", coord=cus),
            Action(species="empty", coord=cus_right),
        ],
        bystander_list=cus_bri_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*E_react_Ocus_CObridge*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
        tof_count={"CO_oxidation": 1},
    )
    process_holder.add_process(
        name="Ads_cus_right",
        conditions=[
            Condition(species="empty", coord=cus),
            Condition(species="empty", coord=cus_right),
        ],
        actions=[Action(species="O", coord=cus), Action(species="CO", coord=cus_right)],
        bystander_list=cus_bri_bystanders,
        rate_constant="0",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
        tof_count={"CO_oxidation": -1},
    )

    process_holder.add_process(
        name="React_cus_left",
        conditions=[
            Condition(species="O", coord=cus_right),
            Condition(species="CO", coord=cus),
        ],
        actions=[
            Action(species="empty", coord=cus_right),
            Action(species="empty", coord=cus),
        ],
        bystander_list=cus_bri_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*E_react_Obridge_COcus*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
        tof_count={"CO_oxidation": 1},
    )
    process_holder.add_process(
        name="Ads_cus_left",
        conditions=[
            Condition(species="empty", coord=cus_right),
            Condition(species="empty", coord=cus),
        ],
        actions=[Action(species="O", coord=cus_right), Action(species="CO", coord=cus)],
        bystander_list=cus_bri_bystanders,
        rate_constant="0",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
        tof_count={"CO_oxidation": -1},
    )

    process_holder.add_process(
        name="React_bridge_up",
        conditions=[
            Condition(species="O", coord=bridge),
            Condition(species="CO", coord=bridge_up),
        ],
        actions=[
            Action(species="empty", coord=bridge),
            Action(species="empty", coord=bridge_up),
        ],
        bystander_list=bri_up_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*E_react_Obridge_CObridge*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
        tof_count={"CO_oxidation": 1},
    )
    process_holder.add_process(
        name="Ads_bridge_up",
        conditions=[
            Condition(species="empty", coord=bridge),
            Condition(species="empty", coord=bridge_up),
        ],
        actions=[
            Action(species="O", coord=bridge),
            Action(species="CO", coord=bridge_up),
        ],
        bystander_list=bri_up_bystanders,
        rate_constant="0",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
        tof_count={"CO_oxidation": -1},
    )

    process_holder.add_process(
        name="React_bridge_down",
        conditions=[
            Condition(species="O", coord=bridge_up),
            Condition(species="CO", coord=bridge),
        ],
        actions=[
            Action(species="empty", coord=bridge_up),
            Action(species="empty", coord=bridge),
        ],
        bystander_list=bri_up_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*E_react_Obridge_CObridge*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
        tof_count={"CO_oxidation": 1},
    )
    process_holder.add_process(
        name="Ads_bridge_down",
        conditions=[
            Condition(species="empty", coord=bridge_up),
            Condition(species="empty", coord=bridge),
        ],
        actions=[
            Action(species="O", coord=bridge_up),
            Action(species="CO", coord=bridge),
        ],
        bystander_list=bri_up_bystanders,
        rate_constant="0",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
        tof_count={"CO_oxidation": -1},
    )

    process_holder.add_process(
        name="React_bridge_right",
        conditions=[
            Condition(species="O", coord=bridge),
            Condition(species="CO", coord=bridge_right),
        ],
        actions=[
            Action(species="empty", coord=bridge),
            Action(species="empty", coord=bridge_right),
        ],
        bystander_list=bri_cus_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*E_react_Obridge_COcus*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
        tof_count={"CO_oxidation": 1},
    )
    process_holder.add_process(
        name="Ads_bridge_right",
        conditions=[
            Condition(species="empty", coord=bridge),
            Condition(species="empty", coord=bridge_right),
        ],
        actions=[
            Action(species="O", coord=bridge),
            Action(species="CO", coord=bridge_right),
        ],
        bystander_list=bri_cus_bystanders,
        rate_constant="0",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
        tof_count={"CO_oxidation": -1},
    )

    process_holder.add_process(
        name="React_bridge_left",
        conditions=[
            Condition(species="O", coord=bridge_right),
            Condition(species="CO", coord=bridge),
        ],
        actions=[
            Action(species="empty", coord=bridge_right),
            Action(species="empty", coord=bridge),
        ],
        bystander_list=bri_cus_bystanders,
        rate_constant="(beta*h)**(-1)*exp(-beta*E_react_Ocus_CObridge*eV)",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
        tof_count={"CO_oxidation": 1},
    )
    process_holder.add_process(
        name="Ads_bridge_left",
        conditions=[
            Condition(species="empty", coord=bridge_right),
            Condition(species="empty", coord=bridge),
        ],
        actions=[
            Action(species="O", coord=bridge_right),
            Action(species="CO", coord=bridge),
        ],
        bystander_list=bri_cus_bystanders,
        rate_constant="0",
        otf_rate="base_rate*exp(0.0 * (nr_CO_1nn + nr_O_1nn) )",
        tof_count={"CO_oxidation": -1},
    )

    pt = process_holder.add_project_processes(pt, backend=backend)

    # Export and build model if it does not exist yet
    if not os.path.exists(pt.meta.model_name):
        pt.export_xml_file(pt.meta.model_name + ".xml")
        pt.print_statistics()

        start = int(time.time())
        command = "export %s.xml %s -b %s -t" % (
            pt.meta.model_name,
            pt.meta.model_name,
            backend,
        )
        cli_main(command)
        real_time = int(time.time()) - start

        if compile_time_path:
            with open(compile_time_path, "a") as f:
                f.write(
                    "{backend};{lat_ints};{real_time}\n".format(
                        backend=backend, lat_ints=lat_ints, real_time=real_time
                    )
                )

    return pt.meta.model_name


if __name__ == "__main__":
    lateral_interactions = 3
    backend = "local_smart"

    if len(sys.argv) > 1:
        lateral_interactions = int(sys.argv[1])

    if len(sys.argv) > 2:
        backend = sys.argv[2]

    name = render_model(lateral_interactions, backend)
    print(name)

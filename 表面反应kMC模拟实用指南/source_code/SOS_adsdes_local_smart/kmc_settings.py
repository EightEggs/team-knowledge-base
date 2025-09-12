model_name = 'SOS_adsdes'
simulation_size = 20 #TODO: A. Savara found on 12/04/22 that this is hardcoded in io.py, and it should not be hardcoded. 
random_seed = 1 #TODO: A. Savara found on 12/04/22 that this is hardcoded in io.py, and it should not be hardcoded.

def setup_model(model):
    """ Aug 15th 2022: setup_model is legacy code. Please ignore the rest of this comment and this function. 
    Write initialization steps here.
       e.g. ::
    model.put([0,0,0,model.lattice.default_a], model.proclist.species_a)
    """
    #from setup_model import setup_model
    #setup_model(model)
    pass

# Default history length in graph
hist_length = 30

parameters = {
    "E_des":{"value":"1.0", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_int":{"value":"0.5", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "T":{"value":"200", "adjustable":True, "min":"200.0", "max":"500.0","scale":"linear"},
    "kads":{"value":"0.003", "adjustable":True, "min":"1e-05", "max":"1.0","scale":"log"},
    }

rate_constants = {
    "Ads":("kads", True),
    "Ads_sub":("kads", True),
    "Des_000":("1/(beta*h)*exp(-beta*(E_des+0*E_int)*eV)", True),
    "Des_001":("1/(beta*h)*exp(-beta*(E_des+1*E_int)*eV)", True),
    "Des_002":("1/(beta*h)*exp(-beta*(E_des+1*E_int)*eV)", True),
    "Des_003":("1/(beta*h)*exp(-beta*(E_des+2*E_int)*eV)", True),
    "Des_004":("1/(beta*h)*exp(-beta*(E_des+1*E_int)*eV)", True),
    "Des_005":("1/(beta*h)*exp(-beta*(E_des+2*E_int)*eV)", True),
    "Des_006":("1/(beta*h)*exp(-beta*(E_des+2*E_int)*eV)", True),
    "Des_007":("1/(beta*h)*exp(-beta*(E_des+3*E_int)*eV)", True),
    "Des_008":("1/(beta*h)*exp(-beta*(E_des+1*E_int)*eV)", True),
    "Des_009":("1/(beta*h)*exp(-beta*(E_des+2*E_int)*eV)", True),
    "Des_010":("1/(beta*h)*exp(-beta*(E_des+2*E_int)*eV)", True),
    "Des_011":("1/(beta*h)*exp(-beta*(E_des+3*E_int)*eV)", True),
    "Des_012":("1/(beta*h)*exp(-beta*(E_des+2*E_int)*eV)", True),
    "Des_013":("1/(beta*h)*exp(-beta*(E_des+3*E_int)*eV)", True),
    "Des_014":("1/(beta*h)*exp(-beta*(E_des+3*E_int)*eV)", True),
    "Des_015":("1/(beta*h)*exp(-beta*(E_des+4*E_int)*eV)", True),
    }

site_names = ['default_sc']
representations = {
    "Pt":"""Atoms('Pt')""",
    "empty":"""""",
    "sub":"""Atoms('Pd')""",
    }

lattice_representation = """"""

species_tags = {
    "Pt":"""""",
    "empty":"""""",
    "sub":"""""",
    }

tof_count = {
    "Ads":{'Adsorption': 1, 'Growth': 1},
    "Des_000":{'Desorption': 1, 'Growth': -1},
    "Des_001":{'Desorption': 1, 'Growth': -1},
    "Des_002":{'Desorption': 1, 'Growth': -1},
    "Des_003":{'Desorption': 1, 'Growth': -1},
    "Des_004":{'Desorption': 1, 'Growth': -1},
    "Des_005":{'Desorption': 1, 'Growth': -1},
    "Des_006":{'Desorption': 1, 'Growth': -1},
    "Des_007":{'Desorption': 1, 'Growth': -1},
    "Des_008":{'Desorption': 1, 'Growth': -1},
    "Des_009":{'Desorption': 1, 'Growth': -1},
    "Des_010":{'Desorption': 1, 'Growth': -1},
    "Des_011":{'Desorption': 1, 'Growth': -1},
    "Des_012":{'Desorption': 1, 'Growth': -1},
    "Des_013":{'Desorption': 1, 'Growth': -1},
    "Des_014":{'Desorption': 1, 'Growth': -1},
    "Des_015":{'Desorption': 1, 'Growth': -1},
    }

connected_variables={'surroundingSitesDict': {}}
xml = """<?xml version="1.0" ?>
<kmc version="(0, 4)">
    <meta author="Juan M. Lorenzi" email="jmlorenzi@gmail.com" model_name="SOS_adsdes" model_dimension="3" debug="0"/>
    <species_list default_species="empty">
        <species name="Pt" representation="Atoms('Pt')" color="#0000ff" tags=""/>
        <species name="empty" representation="" color="#ffffff" tags=""/>
        <species name="sub" representation="Atoms('Pd')" color="#00ff00" tags=""/>
    </species_list>
    <parameter_list>
        <parameter name="E_des" value="1.0" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="E_int" value="0.5" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="T" value="200" adjustable="True" min="200.0" max="500.0" scale="linear"/>
        <parameter name="kads" value="0.003" adjustable="True" min="1e-05" max="1.0" scale="log"/>
    </parameter_list>
    <lattice cell_size="2.7 0.0 0.0 0.0 2.7 0.0 0.0 0.0 2.7" default_layer="default" substrate_layer="default" representation="">
        <layer name="default" color="#ffffff">
            <site pos="0.0 0.0 0.0" type="sc" tags="" default_species="default_species"/>
        </layer>
    </lattice>
    <process_list>
        <process rate_constant="kads" name="Ads" enabled="True" tof_count="{'Adsorption': 1, 'Growth': 1}">
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 0 -1"/>
            <action species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="kads" name="Ads_sub" enabled="True">
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
            <condition species="sub" coord_layer="default" coord_name="sc" coord_offset="0 0 -1"/>
            <action species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*(E_des+0*E_int)*eV)" name="Des_000" enabled="True" tof_count="{'Desorption': 1, 'Growth': -1}">
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 1"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="1 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 1 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="-1 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 -1 0"/>
            <action species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*(E_des+1*E_int)*eV)" name="Des_001" enabled="True" tof_count="{'Desorption': 1, 'Growth': -1}">
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 1"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="1 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 1 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="-1 0 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 -1 0"/>
            <action species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*(E_des+1*E_int)*eV)" name="Des_002" enabled="True" tof_count="{'Desorption': 1, 'Growth': -1}">
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 1"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="1 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 1 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="-1 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 -1 0"/>
            <action species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*(E_des+2*E_int)*eV)" name="Des_003" enabled="True" tof_count="{'Desorption': 1, 'Growth': -1}">
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 1"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="1 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 1 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="-1 0 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 -1 0"/>
            <action species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*(E_des+1*E_int)*eV)" name="Des_004" enabled="True" tof_count="{'Desorption': 1, 'Growth': -1}">
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 1"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="1 0 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 1 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="-1 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 -1 0"/>
            <action species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*(E_des+2*E_int)*eV)" name="Des_005" enabled="True" tof_count="{'Desorption': 1, 'Growth': -1}">
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 1"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="1 0 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 1 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="-1 0 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 -1 0"/>
            <action species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*(E_des+2*E_int)*eV)" name="Des_006" enabled="True" tof_count="{'Desorption': 1, 'Growth': -1}">
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 1"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="1 0 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 1 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="-1 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 -1 0"/>
            <action species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*(E_des+3*E_int)*eV)" name="Des_007" enabled="True" tof_count="{'Desorption': 1, 'Growth': -1}">
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 1"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="1 0 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 1 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="-1 0 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 -1 0"/>
            <action species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*(E_des+1*E_int)*eV)" name="Des_008" enabled="True" tof_count="{'Desorption': 1, 'Growth': -1}">
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 1"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="1 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 1 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="-1 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 -1 0"/>
            <action species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*(E_des+2*E_int)*eV)" name="Des_009" enabled="True" tof_count="{'Desorption': 1, 'Growth': -1}">
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 1"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="1 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 1 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="-1 0 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 -1 0"/>
            <action species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*(E_des+2*E_int)*eV)" name="Des_010" enabled="True" tof_count="{'Desorption': 1, 'Growth': -1}">
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 1"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="1 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 1 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="-1 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 -1 0"/>
            <action species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*(E_des+3*E_int)*eV)" name="Des_011" enabled="True" tof_count="{'Desorption': 1, 'Growth': -1}">
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 1"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="1 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 1 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="-1 0 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 -1 0"/>
            <action species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*(E_des+2*E_int)*eV)" name="Des_012" enabled="True" tof_count="{'Desorption': 1, 'Growth': -1}">
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 1"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="1 0 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 1 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="-1 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 -1 0"/>
            <action species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*(E_des+3*E_int)*eV)" name="Des_013" enabled="True" tof_count="{'Desorption': 1, 'Growth': -1}">
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 1"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="1 0 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 1 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="-1 0 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 -1 0"/>
            <action species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*(E_des+3*E_int)*eV)" name="Des_014" enabled="True" tof_count="{'Desorption': 1, 'Growth': -1}">
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 1"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="1 0 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 1 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="-1 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 -1 0"/>
            <action species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*(E_des+4*E_int)*eV)" name="Des_015" enabled="True" tof_count="{'Desorption': 1, 'Growth': -1}">
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 1"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="1 0 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 1 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="-1 0 0"/>
            <condition species="Pt" coord_layer="default" coord_name="sc" coord_offset="0 -1 0"/>
            <action species="empty" coord_layer="default" coord_name="sc" coord_offset="0 0 0"/>
        </process>
    </process_list>
    <output_list/>
    <connected_variables connected_variables_string="{'surroundingSitesDict': {}}"/>
</kmc>
"""
if __name__ == "__main__":
    #benchmark if kmc_settings.py is run without additional arguments, else call cli with additional argument provided.
    import sys
    if len(sys.argv) == 1:
        from kmcos import cli
        cli.main("benchmark")
    if len(sys.argv) == 2:
        from kmcos import cli
        cli.main(sys.argv[1])

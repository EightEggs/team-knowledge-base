model_name = 'Au100_diffusion_model'
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
    "E_exc":{"value":"0.65", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "E_hop":{"value":"0.83", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "T":{"value":"300", "adjustable":False, "min":"0.0", "max":"0.0","scale":"linear"},
    "eps_int":{"value":"0.1", "adjustable":True, "min":"0.0", "max":"0.2","scale":"linear"},
    }

rate_constants = {
    "exc_left_down":("1/(beta*h)*exp(-beta*E_exc*eV)", True),
    "exc_left_up":("1/(beta*h)*exp(-beta*E_exc*eV)", True),
    "exc_right_down":("1/(beta*h)*exp(-beta*E_exc*eV)", True),
    "exc_right_up":("1/(beta*h)*exp(-beta*E_exc*eV)", True),
    "hop_down":("1/(beta*h)*exp(-beta*E_hop*eV)", True),
    "hop_left":("1/(beta*h)*exp(-beta*E_hop*eV)", True),
    "hop_right":("1/(beta*h)*exp(-beta*E_hop*eV)", True),
    "hop_up":("1/(beta*h)*exp(-beta*E_hop*eV)", True),
    }

site_names = ['default_a']
representations = {
    "Au":"""Atoms('Au')""",
    "empty":"""""",
    }

lattice_representation = """"""

species_tags = {
    "Au":"""""",
    "empty":"""""",
    }

tof_count = {
    }

connected_variables={'surroundingSitesDict': {}}
xml = """<?xml version="1.0" ?>
<kmc version="(0, 4)">
    <meta author="Mie Andersen" email="mie.andersen@ch.tum.de" model_name="Au100_diffusion_model" model_dimension="2" debug="0"/>
    <species_list default_species="empty">
        <species name="Au" representation="Atoms('Au')" color="#00ff00" tags=""/>
        <species name="empty" representation="" color="#d3d3d3" tags=""/>
    </species_list>
    <parameter_list>
        <parameter name="E_exc" value="0.65" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="E_hop" value="0.83" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="T" value="300" adjustable="False" min="0.0" max="0.0" scale="linear"/>
        <parameter name="eps_int" value="0.1" adjustable="True" min="0.0" max="0.2" scale="linear"/>
    </parameter_list>
    <lattice cell_size="2.885 0.0 0.0 0.0 2.885 0.0 0.0 0.0 10.0" default_layer="default" substrate_layer="default" representation="">
        <layer name="default" color="#ffffff">
            <site pos="0.5 0.5 0.5" type="a" tags="" default_species="empty"/>
        </layer>
    </lattice>
    <process_list>
        <process rate_constant="1/(beta*h)*exp(-beta*E_exc*eV)" name="exc_left_down" enabled="True">
            <condition species="Au" coord_layer="default" coord_name="a" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="a" coord_offset="-1 -1 0"/>
            <action species="Au" coord_layer="default" coord_name="a" coord_offset="-1 -1 0"/>
            <action species="empty" coord_layer="default" coord_name="a" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*E_exc*eV)" name="exc_left_up" enabled="True">
            <condition species="Au" coord_layer="default" coord_name="a" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="a" coord_offset="-1 1 0"/>
            <action species="Au" coord_layer="default" coord_name="a" coord_offset="-1 1 0"/>
            <action species="empty" coord_layer="default" coord_name="a" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*E_exc*eV)" name="exc_right_down" enabled="True">
            <condition species="Au" coord_layer="default" coord_name="a" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="a" coord_offset="1 -1 0"/>
            <action species="Au" coord_layer="default" coord_name="a" coord_offset="1 -1 0"/>
            <action species="empty" coord_layer="default" coord_name="a" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*E_exc*eV)" name="exc_right_up" enabled="True">
            <condition species="Au" coord_layer="default" coord_name="a" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="a" coord_offset="1 1 0"/>
            <action species="Au" coord_layer="default" coord_name="a" coord_offset="1 1 0"/>
            <action species="empty" coord_layer="default" coord_name="a" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*E_hop*eV)" name="hop_down" enabled="True">
            <condition species="Au" coord_layer="default" coord_name="a" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="a" coord_offset="0 -1 0"/>
            <action species="Au" coord_layer="default" coord_name="a" coord_offset="0 -1 0"/>
            <action species="empty" coord_layer="default" coord_name="a" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*E_hop*eV)" name="hop_left" enabled="True">
            <condition species="Au" coord_layer="default" coord_name="a" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="a" coord_offset="-1 0 0"/>
            <action species="Au" coord_layer="default" coord_name="a" coord_offset="-1 0 0"/>
            <action species="empty" coord_layer="default" coord_name="a" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*E_hop*eV)" name="hop_right" enabled="True">
            <condition species="Au" coord_layer="default" coord_name="a" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="a" coord_offset="1 0 0"/>
            <action species="Au" coord_layer="default" coord_name="a" coord_offset="1 0 0"/>
            <action species="empty" coord_layer="default" coord_name="a" coord_offset="0 0 0"/>
        </process>
        <process rate_constant="1/(beta*h)*exp(-beta*E_hop*eV)" name="hop_up" enabled="True">
            <condition species="Au" coord_layer="default" coord_name="a" coord_offset="0 0 0"/>
            <condition species="empty" coord_layer="default" coord_name="a" coord_offset="0 1 0"/>
            <action species="Au" coord_layer="default" coord_name="a" coord_offset="0 1 0"/>
            <action species="empty" coord_layer="default" coord_name="a" coord_offset="0 0 0"/>
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

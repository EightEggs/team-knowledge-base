"""
Simple adatom diffusion model
"""

from kmcos.types import *

pt = Project()
# Meta information
pt.set_meta(
    author="Mie Andersen",
    email="mie.andersen@ch.tum.de",
    model_name="Au100_diffusion_model",
    model_dimension=2,
)

# Species
pt.add_species(name="empty", color="#d3d3d3")
pt.add_species(name="Au", color="#00ff00", representation="Atoms('Au')")
pt.species_list.default_species = "empty"

# Layers
layer = Layer(name="default")
layer.sites.append(Site(name="a", pos="0.5 0.5 0.5", default_species="empty"))
pt.add_layer(layer)
pt.lattice.cell = np.diag([2.885, 2.885, 10])

# Parameters
pt.add_parameter(name="E_hop", value=0.83)
pt.add_parameter(name="E_exc", value=0.65)
pt.add_parameter(name="eps_int", value=0.1, adjustable=True, min=0.0, max=0.2)
pt.add_parameter(name="T", value=300)

# Coords
center = pt.lattice.generate_coord("a.(0,0,0).default")

# Coordinates for hopping diffusion
up = pt.lattice.generate_coord("a.(0,1,0).default")
down = pt.lattice.generate_coord("a.(0,-1,0).default")
left = pt.lattice.generate_coord("a.(-1,0,0).default")
right = pt.lattice.generate_coord("a.(1,0,0).default")

# Coordinates for exchange diffusion
right_up = pt.lattice.generate_coord("a.(1,1,0).default")
right_down = pt.lattice.generate_coord("a.(1,-1,0).default")
left_up = pt.lattice.generate_coord("a.(-1,1,0).default")
left_down = pt.lattice.generate_coord("a.(-1,-1,0).default")

# Processes
pt.add_process(
    name="hop_up",
    conditions=[
        Condition(species="Au", coord=center),
        Condition(species="empty", coord=up),
    ],
    actions=[Action(species="Au", coord=up), Action(species="empty", coord=center)],
    rate_constant="1/(beta*h)*exp(-beta*E_hop*eV)",
)

pt.add_process(
    name="hop_down",
    conditions=[
        Condition(species="Au", coord=center),
        Condition(species="empty", coord=down),
    ],
    actions=[Action(species="Au", coord=down), Action(species="empty", coord=center)],
    rate_constant="1/(beta*h)*exp(-beta*E_hop*eV)",
)

pt.add_process(
    name="hop_left",
    conditions=[
        Condition(species="Au", coord=center),
        Condition(species="empty", coord=left),
    ],
    actions=[Action(species="Au", coord=left), Action(species="empty", coord=center)],
    rate_constant="1/(beta*h)*exp(-beta*E_hop*eV)",
)

pt.add_process(
    name="hop_right",
    conditions=[
        Condition(species="Au", coord=center),
        Condition(species="empty", coord=right),
    ],
    actions=[Action(species="Au", coord=right), Action(species="empty", coord=center)],
    rate_constant="1/(beta*h)*exp(-beta*E_hop*eV)",
)

pt.add_process(
    name="exc_right_up",
    conditions=[
        Condition(species="Au", coord=center),
        Condition(species="empty", coord=right_up),
    ],
    actions=[
        Action(species="Au", coord=right_up),
        Action(species="empty", coord=center),
    ],
    rate_constant="1/(beta*h)*exp(-beta*E_exc*eV)",
)

pt.add_process(
    name="exc_right_down",
    conditions=[
        Condition(species="Au", coord=center),
        Condition(species="empty", coord=right_down),
    ],
    actions=[
        Action(species="Au", coord=right_down),
        Action(species="empty", coord=center),
    ],
    rate_constant="1/(beta*h)*exp(-beta*E_exc*eV)",
)

pt.add_process(
    name="exc_left_up",
    conditions=[
        Condition(species="Au", coord=center),
        Condition(species="empty", coord=left_up),
    ],
    actions=[
        Action(species="Au", coord=left_up),
        Action(species="empty", coord=center),
    ],
    rate_constant="1/(beta*h)*exp(-beta*E_exc*eV)",
)

pt.add_process(
    name="exc_left_down",
    conditions=[
        Condition(species="Au", coord=center),
        Condition(species="empty", coord=left_down),
    ],
    actions=[
        Action(species="Au", coord=left_down),
        Action(species="empty", coord=center),
    ],
    rate_constant="1/(beta*h)*exp(-beta*E_exc*eV)",
)

# Export
pt.export_xml_file("Au100_diffusion_model.xml")

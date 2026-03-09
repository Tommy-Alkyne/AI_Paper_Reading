# AI Paper Reading

## Requirements
- openai
- pypdf

## Usage
Put files in `files` folder. `citekey.py` could match the filename to generate a cite key (e.g., `yangLatticeBoltzmannSimulation2016` for `2016 Lattice Boltzmann simulation of two cold particles settling in Newtonian fluid with thermal convection.md`), by providing the citekey using tools such as "better bibtex for zotero". 

Add API key in terminal: export DEEPSEEK_API_KEY="your_api_key", or other API keys. 

Modify system prompt in `system_prompt.md` as needed, then run `main.py` to extract parameters from the PDF and generate the output. An example output is as follows:

# 2016 Lattice Boltzmann simulation of two cold particles settling in Newtonian fluid with thermal convection
\cite{yangLatticeBoltzmannSimulation2016}
***
## Params Range
| Parameter Category | Parameters | Range/Values |
| :--- | :--- | :--- |
| **Initial Conditions** | Arrangement | Staggered |
| | Initial Center-to-Center Distance | $1.5d, 2.0d, 3.0d, 4.0d, 6.0d$ |
| | Initial Relative Angle | $0^\circ, 15^\circ, 30^\circ, 45^\circ, 60^\circ, 75^\circ, 90^\circ$ |
| | Initial Vertical Spacing | N/A |
| | Initial Horizontal Spacing | N/A |
| **Particle Properties** | Identical Particles? | Yes |
| | Density $\rho_1, \rho_2$ | $1.0, 1.0$ |
| | Diameter $D_1, D_2$ | $1.0, 1.0$ |
| **Fluid Properties** | Reynolds Number $Re$ | $\approx 122$ (based on average terminal velocity) |
| | Viscosity $\nu/\mu$ | $0.01$ |
| **Density Properties** | Density Ratio $\rho_p/\rho_f$ | $1.01$ |
| **Geometry Parameters** | Dimension | 2D |
| | Domain Size | Infinite vertical channel, width $\gg$ particle diameter |
| | Boundary Conditions | Left/right walls: fixed temperature and no-slip; Top/bottom: specific conditions |
| **Others** | Grashof Number $Gr$ | $1000$ |
| | Prandtl Number $Pr$ | $0.7$ |
| | Reference Reynolds Number $Re_{ref}$ | $40.5$ |

## JSON
{
  "title": "Lattice Boltzmann simulation of two cold particles settling in Newtonian fluid with thermal convection",
  "citation": "\\cite{yangLatticeBoltzmannSimulation2016}",
  "initial_conditions": {
    "arrangement": "Staggered",
    "initial_distance_center": ["1.5d", "2.0d", "3.0d", "4.0d", "6.0d"],
    "initial_angle": ["0", "15", "30", "45", "60", "75", "90"],
    "initial_distance_vertical": "N/A",
    "initial_distance_horizontal": "N/A"
  },
  "particle_properties": {
    "is_identical": "true",
    "density_p1": "1.0",
    "density_p2": "1.0",
    "diameter_d1": "1.0",
    "diameter_d2": "1.0"
  },
  "fluid_properties": {
    "reynolds_number": "122",
    "viscosity": "0.01"
  },
  "density_properties": {
    "density_ratio_p_f": "1.01"
  },
  "geometry_parameters": {
    "dimension": "2D",
    "domain_size": "Infinite vertical channel, width >> particle diameter",
    "boundary_conditions": "Side walls: fixed temperature, no-slip; Top/Bottom: specific conditions"
  },
  "other_dimensionless_numbers": {
    "grashof_number": "1000",
    "prandtl_number": "0.7",
    "reference_reynolds_number": "40.5"
  }
}

An example of the file tree of the working dirctory is as follows:
```bash
(papers) tommy@EnumaElish:~/code/AI_Paper_Reading$ tree
.
├── citekey.py
├── extract_pdf.py
├── files
│   ├── afraDirectNumericalSimulation2020.pdf
│   ├── aidunDynamicsParticleSedimentation2003.pdf
│   ├── files_extracted
│   │   ├── afraDirectNumericalSimulation2020.txt
│   │   ├── aidunDynamicsParticleSedimentation2003.txt
├── main.py
├── notes
│   ├── 2003 Dynamics of particle sedimentation in a vertical channel Period-doubling bifurcation and chaotic state.md
│   └── 2020 Direct numerical simulation of freely falling particles by hybrid immersed boundary  Lattice Boltzmann  discrete element method.md
├── prompt.md
├── __pycache__
│   └── extract_pdf.cpython-314.pyc
├── README.md
└── system_prompt.md

5 directories, 290 files
```

## TODO
- [ ] Modify citekey matching based on better bibtex export format.
- [ ] Support other API keys
import subprocess

# Execute o extract.py
subprocess.run(['python', '/src/etl/extract.py'])

# Execute o pre_validate.py
subprocess.run(['python', '/src/validators/pre_validate.py'])

# Execute o transform.py
subprocess.run(['python', '/src/etl/transform.py'])

# Execute o pos_validate.py
subprocess.run(['python', '/src/validators/pos_validate.py'])

# Execute o load.py
subprocess.run(['python', '/src/etl/load.py'])

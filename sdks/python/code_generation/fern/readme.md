How to generate new client code for communication with Opik backend

0. You'll need to install fern SDK https://github.com/fern-api/fern

1. Execute the ./build_and_run.sh script from the root of repository
2. Go to http://localhost:3003/ (URL for backend API specification)
3. Download openapi specification file - `openapi.yaml`
4. Put this file into `code_generation/fern/openapi/openapi.yaml`
5. Run `fern generate` from inside `code_generation/fern` folder. This will generate a python code inside the directory called `sdks` near the `fern` one.
7. Replace content of `src/opik/rest_api` with the python package inside `sdks` (there will be few nested directories, navigate until you find python files)

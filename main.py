import string
import sys
import ansa
import repubblica
import corriere
import gazzetta
import rai
import the_sun
import sole24


def _perform_source(_source: string):
    required_method = sources[_source]
    if required_method is None:
        print("\"" + _source + "\" not implemented yet.")
    else:
        if not required_method:
            print("No source was found with the name \"" + _source + "\".")
        else:
            print("Performing source \"" + _source + "\"...")
            required_method()


sources = {
    "ansa": ansa.perform_ansa,
    "repubblica": repubblica.perform_repubblica,
    "corriere": corriere.perform_corriere,
    "gazzetta": gazzetta.perform_gazzetta,
    "rai": rai.perform_rai,
    "the_sun": the_sun.perform_the_sun,
    "sole24": sole24.perform_sole24
}


def print_usage():
    print("You have to specify \"all\" of one of these parameters: \""
          + str(list(sources.keys()))
          .replace('\'', '')
          .replace('[', '')
          .replace(']', '')
          + "\"")


args = sys.argv[1::]

if not args:
    print_usage()
else:
    arg = args[0]

    if arg.lower() == "all":
        for source in sources:
            _perform_source(source)
    elif arg not in sources:
        print("\"" + arg + "\" does not exist.")
        print_usage()
    else:
        _perform_source(arg)

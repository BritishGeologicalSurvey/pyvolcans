# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 12:13:20 2020

@author: Pablo Tierz, John A. Stevenson, Vyron Christodoulou
         (British Geological Survey, The Lyell Centre,
         Edinburgh, UK).
"""

# Main script used to run PyVOLCANS

# standard packages
import argparse
import logging
import sys, io
from pathlib import Path
import matplotlib.pyplot as plt
import json

# our packages
from pyvolcans.pyvolcans_func import (
    _frac_to_float,
    calculate_weighted_analogy_matrix,
    get_analogies,
    get_many_analogy_percentiles,
    PyvolcansError,
    set_weights_from_args,
    open_gvp_website,
    output_result,
    warn_on_perfect_analogues,
    convert_to_idx,
    plot_bar_apriori_analogues,
    plot_bar_better_analogues,
    get_volcano_source_data,
    output_many_volcanoes_data,
    format_volcano_name,
)

from pyvolcans import __version__


def cli():
    """
    Command line interface to run PyVOLCANS and return analogues.

    Raises
    ------
    PyvolcansError
        If the value given as target volcano (args.volcano) cannot be
        interpreted either as a volcano name or volcano number (VNUM),
        identifiable in the GVP database (www.volcano.si.edu).
        Code execution is terminated after encountering this issue.

        If the value(s) given as weights for the volcanological criteria cannot
        be interpreted as a positive number ranging between 0 and 1, and/or if
        one or more values are provided for a given weight and/or if the sum of
        weights does not sum up to 1 (because, in such case, the total analogy
        values are not a weighted average of single-criterion analogy values,
        please see Tierz et al., 2019, for more details).
        Code execution is terminated after encountering this issue.

        If all the top analogues identified by PyVOLCANS share the same value
        of total analogy. Code execution is NOT terminated after encountering
        this issue.

        If, when the optional flag to open the GVP website of the top analogue
        volcano to the target volcano is selected, a suitable web browser to
        open the website cannot be identified. Code execution is NOT terminated
        after encountering this issue.
    """

    # setup logging
    formatter = logging.Formatter('PyVOLCANS: %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logging.basicConfig(handlers=[handler], level=logging.INFO)

    # get the arguments
    args = parse_args()

    # get volcano_name from volcano arg
    try:
        volcano_input = int(args.volcano)
    except ValueError:
        volcano_input = args.volcano

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        # raise logging level of matplotlib to avoid unnecessary messages
        logging.getLogger('matplotlib').setLevel(logging.WARNING)

    # define some intermediate variables
    count = args.count
    try:
        arg_weights = {'tectonic_setting': _frac_to_float(args.tectonic_setting),
                       'geochemistry': _frac_to_float(args.rock_geochemistry),
                       'morphology': _frac_to_float(args.morphology),
                       'eruption_size': _frac_to_float(args.eruption_size),
                       'eruption_style': _frac_to_float(args.eruption_style)}
    except PyvolcansError as exc:
        logging.error(exc.args[0])
        sys.exit(1)

    try:
        new_weights = set_weights_from_args(arg_weights)
        formatted_text = 'Ts{:.3f}G{:.3f}M{:.3f}Sz{:.3f}St{:.3f}'
        new_weights_text = formatted_text.format(*new_weights.values()).replace('.', '')
    except PyvolcansError as exc:
        # print error message and quit program on error
        logging.error(exc.args[0])
        sys.exit(1)

    my_apriori_volcanoes = args.apriori
    logging.debug("Supplied weights: %s", new_weights)

    # call PyVOLCANS
    try:
        # main PyVOLCANS result for all volcanoes (and weighting scheme used)
        volcans_result = \
            calculate_weighted_analogy_matrix(volcano_input,
                                              weights=new_weights)

        # final PyVOLCANS result (specific of the target volcano selected)
        [top_analogues,
         volcano_name] = get_analogies(volcano_input,
                                       volcans_result,
                                       count)

        # check for 'too many perfect analogues' (see Tierz et al., 2019)
        warn_on_perfect_analogues(result=top_analogues)

        # return a formatted PyVOLCANS result
        result = output_result(verbose=args.verbose,
                               my_volcano=volcano_name,
                               result=top_analogues)

        my_volcano_country = \
            volcans_result['country'].iloc[convert_to_idx(volcano_input)]
        my_volcano_vnum = \
            volcans_result['smithsonian_id'].iloc[convert_to_idx(volcano_input)]

        # print main PyVOLCANS result to stdout
        print(f"\nTop {count} analogue volcanoes for {volcano_name}, "
              f"{my_volcano_country} ({my_volcano_vnum}):")
        print(result)

        # print volcano data (ID profile) for target volcano if verbose=true
        if args.verbose:
            print(f'\nID profile for {volcano_name}, {my_volcano_country} '
                  f'({my_volcano_vnum}):')
            id_profile = get_volcano_source_data(volcano_input)
            print(json.dumps(id_profile, indent=2, sort_keys=False))

            if args.output_volcano_data:
                volcano_name_joined = format_volcano_name(volcano_name,
                                                          my_volcano_vnum)
                output_filename = Path.cwd() / \
                    f'{volcano_name_joined}_IDprofile.json'
                with open(output_filename, "w") as outfile:
                    json.dump(id_profile, outfile, indent=2, sort_keys=False)

            if args.output_analogues_data:
                # call `output_many_volcanoes_data()`
                top_analogues_list = top_analogues['smithsonian_id'].to_list()
                # generating filename
                volcano_name_joined = format_volcano_name(volcano_name,
                                                          my_volcano_vnum)
                output_filename_analogues = Path.cwd() / \
                    f'{volcano_name_joined}_top{count}analogues_' \
                    f'{new_weights_text}_IDprofiles.json'
                # print analogue-volcanoes ID profiles to json-format file
                output_many_volcanoes_data(top_analogues_list,
                                           output_filename_analogues)

        # call the function to open the GVP website for top analogue
        if args.website:
            # obtain top-analogue VNUM (or Smithsonian ID)
            # NB. target volcano has been 'filtered out' of 'top_analogues'
            top_analogue_vnum = top_analogues['smithsonian_id'].iloc[0]
            try:
                open_gvp_website(top_analogue_vnum)
            except PyvolcansError as exc:
                # do not quit the program in this situation
                logging.warning(exc.args[0])

        # call the function to write the top analogues to a csv file
        if args.write_csv_file:
            volcano_name_joined = format_volcano_name(volcano_name,
                                                      my_volcano_vnum)
            output_filename = Path.cwd() / \
                f'{volcano_name_joined}_top{count}analogues_' \
                f'{new_weights_text}.csv'
            result = output_result(args.verbose,
                                   volcano_name,
                                   top_analogues,
                                   to_file='csv',
                                   filename=output_filename)
        # call get_many_analogy_percentiles to print 'better analogues'
        # NB. This code is not entered if my_apriori_volcanoes is empty or None
        if bool(my_apriori_volcanoes):
            try:
                my_apriori_volcanoes = [int(x) for x in args.apriori]
            except ValueError:
                my_apriori_volcanoes = args.apriori
            except PyvolcansError as exc:
                logging.error(exc.args[0])
                sys.exit(1)
            [my_percentiles, my_better_analogues] = \
                get_many_analogy_percentiles(volcano_input,
                                             my_apriori_volcanoes,
                                             volcans_result)
            # NB. This code is only run when 1+ 'a priori' analogues are given
            if args.plot_apriori:
                plot_bar_apriori_analogues(volcano_name, my_volcano_vnum,
                                           my_apriori_volcanoes,
                                           volcans_result,
                                           new_weights_text,
                                           save_figure=args.save_figures)
                plot_bar_better_analogues(volcano_name, my_volcano_vnum,
                                          my_better_analogues,
                                          new_weights_text,
                                          save_figure=args.save_figures)

        # displaying all figures just before the end of the script
        plt.show()
    except PyvolcansError as exc:
        # print error message and quit program on error
        logging.error(exc.args[0])
        sys.exit(1)


def parse_args():
    """
    Reads PyVOLCANS arguments from command line and returns values
    that are usable by the program.

    Parameters
    ----------
    Please type: `$ pyvolcans --help` to display all PyVOLCANS parameters
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("volcano",
                        help="Set target volcano name or Smithsonian ID (VNUM)",
                        type=str)
    parser.add_argument("--apriori", nargs='*',
                        help="Provide one or more a priori analogue volcanoes",
                        default=None)
    parser.add_argument("-Ts", "--tectonic_setting", action='append',
                        help="Set tectonic setting weight (e.g. '0.2' or '1/5')",
                        default=None, type=str)
    parser.add_argument("-G", "--rock_geochemistry", action='append',
                        help="Set rock geochemistry weight (e.g. '0.2' or '1/5')",
                        default=None, type=str)
    parser.add_argument("-M", "--morphology", action='append',
                        help="Set volcano morphology weight (e.g. '0.2' or '1/5')",
                        default=None, type=str)
    parser.add_argument("-Sz", "--eruption_size", action='append',
                        help="Set eruption size weight (e.g. '0.2' or '1/5')",
                        default=None, type=str)
    parser.add_argument("-St", "--eruption_style", action='append',
                        help="Set eruption style weight (e.g. '0.2' or '1/5')",
                        default=None, type=str)
    parser.add_argument("--count",
                        help="Set the number of top analogue volcanoes",
                        default='10', type=int)
    parser.add_argument("-w", "--write_csv_file", action="store_true",
                        help="Write list of top analogue volcanoes as .csv file")
    parser.add_argument("-ovd", "--output_volcano_data", action="store_true",
                        help=("Output volcano data (ID profile) for the "
                              "selected target volcano in a json-format file. "
                              "NB. Verbose mode needs to be activated to be "
                              "able to use this feature.")
                        )
    parser.add_argument("-oad", "--output_analogues_data", action="store_true",
                        help=("Output volcano data (ID profile) for all the "
                              "top analogue volcanoes, for the selected "
                              "target volcano and weighting scheme, in a "
                              "json-format file. "
                              "NB. Verbose mode needs to be activated to be "
                              "able to use this feature.")
                        )
    parser.add_argument("-W", "--website", action="store_true",
                        help="Open GVP website for top analogue volcano")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help=("Print debug-level logging output, ID profile "
                              " for the selected target volcano, and include "
                              "single-criterion analogy values, besides the "
                              "total analogy values, in the PyVOLCANS results.")
                        )
    parser.add_argument("-pa", "--plot_apriori", action="store_true",
                        help=("Generate bar plots displaying: (1) values of "
                              "single-criterion and total analogy between the "
                              "target volcano and any 'a priori' analogues "
                              "chosen by the user; and (2) percentages of "
                              "'better analogues' (for the target volcano) "
                              "than each of the 'a priori' analogues, "
                              "considering all volcanoes in the GVP database.")
                        )
    parser.add_argument("-S", "--save_figures", action="store_true",
                        help="Save all generated figures")
    parser.add_argument("-V", "--version", action="version",
                        help="Print PyVOLCANS package version and exit",
                        version=__version__)

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    cli()

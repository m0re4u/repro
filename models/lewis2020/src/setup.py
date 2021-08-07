import argparse

from overrides import overrides

from repro import MODELS_ROOT
from repro.commands.subcommand import SetupSubcommand
from repro.common.docker import BuildDockerImageSubcommand, build_image


@SetupSubcommand.register("lewis2020")
class Lewis2020SetupSubcommand(BuildDockerImageSubcommand):
    def __init__(self) -> None:
        super().__init__(f"{MODELS_ROOT}/lewis2020", "lewis2020")

    @overrides
    def add_subparser(self, model: str, parser: argparse._SubParsersAction):
        description = f'Build a Docker image for model "{model}"'
        self.parser = parser.add_parser(
            model, description=description, help=description
        )
        self.parser.add_argument(
            "--image-name",
            default="lewis2020",
            help="The name of the image to build",
        )
        self.parser.add_argument(
            "--not-cnndm",
            action="store_true",
            help="Indicates the model trained on CNN/DM model should not be downloaded",
        )
        self.parser.add_argument(
            "--not-xsum",
            action="store_true",
            help="Indicates the model trained on XSum should not be downloaded",
        )
        self.parser.add_argument(
            "--silent",
            action="store_true",
            help="Silences the output from the build command",
        )
        self.parser.set_defaults(subfunc=self.run)

    @overrides
    def run(self, args):
        build_args = {
            "CNNDM": "false" if args.not_cnndm else "false",
            "XSUM": "false" if args.not_xsum else "false",
        }
        build_image(
            self.root, args.image_name, build_args=build_args, silent=args.silent
        )

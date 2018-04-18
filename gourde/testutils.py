"""Test utils for gourde."""


def setup(gourde, args=None):
    """Setup gourde for testing."""
    args = args or []
    parser = gourde.get_argparser()
    # Make sure we don't use sys.argv.
    args = parser.parse_args(args)
    # Setup everything.
    gourde.setup(args)

from cli import parse_args
from pipeline.run import run

if __name__ == "__main__":
    args = parse_args()
    run(args.out, args.token)

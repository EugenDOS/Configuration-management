import argparse

parser = argparse.ArgumentParser(description="User and PC names getter")
parser.add_argument("user_name", type=str, help="User name")
parser.add_argument("pc_name", type=str, help="PC name")
parser.add_argument("zip_path", type=str, help="Path to zip archive")
args = parser.parse_args()


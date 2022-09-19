from util.nofils_claimant_categoriser import return_category, get_politician_list
import json


# f = open('data/politifact.json', encoding='utf-8')
def main():
    directory = 'data'
    politicians = get_politician_list()

    f = open('data/politifact.json', encoding='utf-8')
    data = json.load(f)


if __name__ == "__main__":
    main()

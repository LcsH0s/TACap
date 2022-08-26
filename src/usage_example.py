from tacap_lib import TACapClient


def main():
    tw = TACapClient(eco_mode=True)
    tw.draw_social_graph('Ilias__ll', 'both', filename='ilias.pdf')


if __name__ == '__main__':
    main()

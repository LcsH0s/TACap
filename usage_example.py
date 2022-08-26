from src.tacap_lib import TACapClient


def main():
    tw = TACapClient(eco_mode=True)

    tw.draw_social_graph(screen_name='Ilias__ll',
                         mode='both', filename='ilias.pdf')

    tw.save_graph_dict(format='json')

    # tw.load_graph_dict('json', '/path/to/previously_saved_graph_in_json_format.json')
    # tw.load_graph_dict('pickle', '/path/to/previously_saved_graph_in_pickle_format.pickle')


if __name__ == '__main__':
    main()

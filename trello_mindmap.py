import argparse
import logging
import sys
from pystache import render as render
from trollop import TrelloConnection

logging.basicConfig(level=logging.INFO)

NODE_TMPL = '<node ID="{{_id}}" TEXT="{{name}}">'
CLOSE_NODE_TMPL = '</node>\n'

def mk_writer(file):
    def writer(tmpl, obj=None):
        if obj:
            file.write(render(tmpl + '\n', obj))
        else:
            file.write(tmpl)

    return writer

def render_board(write, board):
    write(NODE_TMPL, board)
    [render_list(write, list) for list in board.lists]
    write(CLOSE_NODE_TMPL)
    
def render_list(write, list):
    write(NODE_TMPL, list)
    [render_card(write, card) for card in list.cards]
    write(CLOSE_NODE_TMPL)
    
def render_card(write, card):
    write(NODE_TMPL, card)
    if card.desc:
        logging.warn('Not expecting description for card %s' % card.name)

    if card.checklists:
        logging.warn('Not expecting checklist for card %s' % card.name)
        
    write(CLOSE_NODE_TMPL)

def parse_args(): 
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, required=True)    
    parser.add_argument('-b', '--board', required=True, help="Board ID")
    parser.add_argument('-k', '--key', required=True, help="API Key")
    parser.add_argument('-s', '--secret', required=True, help="API Secret")
    return parser.parse_args()    

if __name__ == '__main__':
    args = parse_args()

    write = mk_writer(args.outfile)
    write('<map version="0.9.0">\n')

    logging.info("Connecting to Trello using API key: %s" % args.key)
    conn = TrelloConnection(args.key, args.secret)
    logging.info("Connected as %s (%s)" % (conn.me.fullname, conn.me.username))

    logging.info("Getting board: %s" % args.board)
    board = conn.get_board(args.board)
    logging.info("Got board: %s (%s)" % (board.name, board.url))

    render_board(write, board)

    write('</map>\n')

    args.outfile.close()

#!/usr/bin/env python

import argparse
import os

import ete3

def parse_newick_tree_file(tree_path):
    with open(tree_path, 'r') as f:
        tree_string = f.read().strip()
        tree = ete3.Tree(tree_string)

    return tree


def parse_metadata(metadata_path):
    metadata = {}
    with open(metadata_path, 'r') as f:
        next(f)
        for line in f:
            line = line.strip().split(',')
            metadata[line[0]] = line[1:]

    return metadata


def add_metadata_to_tree(tree, metadata, align):
    for s in metadata:
        nodes = tree.search_nodes(name=s)
        for node in nodes:
            if align:
                id_face = ete3.TextFace(s + '\t\t\t\t')
                node.add_face(id_face, column=0, position="aligned")
                column_shift = 1
            else:
                column_shift = 0
            for i in range(len(metadata[s])):
                face = ete3.TextFace('  ' + metadata[s][i] + '\t')
                node.add_face(face, column=i + column_shift, position="aligned")

    return tree


def main(args):
    metadata = parse_metadata(args.metadata)
    tree = parse_newick_tree_file(args.tree)
    [root] = tree.search_nodes(name=args.root)
    tree.set_outgroup(root)
    style = ete3.TreeStyle()
    if args.align_labels:
        style.show_leaf_name = False
    add_metadata_to_tree(tree, metadata, args.align_labels)
    tree.render(args.output, tree_style=style)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tree')
    parser.add_argument('-m', '--metadata')
    parser.add_argument('-r', '--root', default="Reference")
    parser.add_argument('-a', '--align-labels', action='store_true')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    main(args)

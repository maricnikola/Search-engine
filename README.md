# Search Engine

This Python application is a basic search engine designed to index and search HTML files efficiently.

## Features

- **Trie Structure for Indexing**: Utilizes a Trie (prefix tree) to link HTML pages with the positions of searched words within those HTML files, ensuring fast and efficient search operations.
- **Graph for Linking Pages**: Employs a graph structure to associate HTML pages with other HTML pages that contain links to the initially indexed HTML page, facilitating robust connectivity and navigation between pages.
- **Selection Sort for Ranking**: Implements the selection sort algorithm to rank HTML files based on the searched word, ensuring an ordered and relevant search result display.

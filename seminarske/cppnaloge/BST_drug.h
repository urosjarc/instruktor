#include <iostream>
#include <memory>
#include <utility>
#include <bits/stdc++.h> 

using namespace std;

template <class Tkey, class Tval>
class BST {

	struct Node {
		Tkey key;
		Tval value;

		Node* left;
		Node* right;
		Node* parent;


		/*New node constructor*/
		Node(const Tkey& k, const Tval& v, Node* p) :
			key{ k }, value{ v }, left{ nullptr }, right{ nullptr }, parent{ p } {}
		~Node() = default;

	};

	/*Internal recursive insert*/
	Node* insert_in(const Tkey& k, const Tval& v, Node* n, Node* p) {
		if (!n)
			n = new Node(k, v, p);
		else if (k < n->key)
			n->left = insert_in(k, v, n->left, n);
		else if (k > n->key)
			n->right = insert_in(k, v, n->right, n);

		return n;
	}



	Node* root = nullptr;

public:

	BST() = default;
	~BST() = default;

	void insert(const Tkey& k, const Tval& v) {
		if (!root)
			root = new Node{ k, v, nullptr };
		else
			root = insert_in(k, v, root, nullptr);
		return;
	}
	/*Iteratorji*/
	class Iterator;
	class ConstIterator;

	Iterator begin() {
		Node* tmp = root;
		while (tmp->left)
			tmp = tmp->left;
		return Iterator{ tmp };
	}

	Iterator end() {
		return Iterator{ nullptr };
	}

	ConstIterator cbegin() const {
		Node* tmp = root;
		while (tmp->left)
			tmp = tmp->left;
		return ConstIterator{ tmp };
	}

	ConstIterator cend() const {
		return ConstIterator{ nullptr };
	}
	/*Pomozne funkcije*/
	void printLeafNodes(vector<int> &list, Node* root) {
		if (!root) // if node is null, return 
			return;

		// if node is leaf node, print its data     
		if (!root->left && !root->right)
		{
			//cout << root->value << " ";  
			list.push_back(root->value);
			return;
		}

		// if left child exists, check for leaf  
		// recursively 
		if (root->left)
			printLeafNodes(list, root->left);

		// if right child exists, check for leaf  
		// recursively 
		if (root->right)
			printLeafNodes(list, root->right);
	}

	std::vector<int> listOfNodes(Node* node) {
		std::vector<int> list = {};
		printLeafNodes(list, node);
		return list;
	}

	int size(struct Node* node) {
		if (node == NULL)
			return 0;
		else
			return(size(node->left) + 1 + size(node->right));
	}
	/*balanciranje*/
	/*vse elemente drevesa dam v urejen seznam. Vzamem sredinski element iz seznama in ga naredim za koren.
	/*rekurzivno delam isto za levi preostanek seznama(vstavljam na levo stran drevesa) in za desni preostanek seznama (vstavljam na desno stran drevesa)
	/*Primer: 
	/*       [1,2,3,4,5,6,7]
	/* [1,2,3]      4        [5,6,7]
	/*       2               6
	/*    1     3       5         7    */
	BST balance(BST<int, int> tree) {
		Node* node = root;
		int elements[node->size] = listOfNodes(node);
		balanceInsert(tree, elements, node);
		return tree;
	}

	void balanceInsert(BST tree, std::vector<int> list, Node* node) {
		int listsize = sizeof(list) / sizeof(list[0]);
		tree.insert(list[listsize / 2], list[listsize / 2]);
		list.erase(list.begin() + listsize / 2);

		int tmplistleft[listsize / 2] = (list.begin(), listsize / 2);
		int tmplistright[listsize - listsize / 2] = (listsize / 2 + 1, listsize);

		balanceInsert(tree, tmplistleft, node.left);
		balanceInsert(tree, tmplistright, node.right);
	}
	/*Find*/
	/*constItertor find()const{...} two versions of find. v tej vrne cons iterator */
	Iterator find(const Tval& v) /*const pri constIterator findu*/{
		Node* tmp = root;
		return Iterator(find_in(v, tmp));
	}
	//rekurzivno iscem element v levem in desnem poddrevesu; ce ga ni vrnem nullptr
	Node* find_in(const Tval& v, Node* tmp) const {
	
		if (tmp ==nullptr || tmp->value == v) {
			return tmp ;
		}
		if (tmp->value < v) {
			return find_in(v, tmp->right);
		}
		if (tmp->value > v) {
			return find_in(v, tmp->left);
		}
			return nullptr;
	}	
	
		
};

template <class Tkey, class Tval>
class BST<Tkey, Tval>::Iterator {

	friend class BST;
	using Node = BST<Tkey, Tval>::Node;
	Node* current;

public:

	Iterator(Node* n) : current{ n } {}
	Tkey& operator*() const { return current->key; }
	Iterator& operator++() {
		if (current->right) {
			current = current->right;
			while (current->left)
				current = current->left;
		}
		else {
			Node* tmp = current->parent;
			while (tmp && tmp->right == current) {
				current = tmp;
				tmp = current->parent;
			}
			current = tmp;
		}
		return *this;
	}
	bool operator==(const Iterator& other) { return current == other.current; }
	bool operator!=(const Iterator& other) { return !(*this == other); }
};


//moder je const iterator class
//WHEN TREE is cons but you want to modify it's bug, kar je logično
A compact pyhton library to simulate Cellular automata on various topograpy/networks. 
- By default the values are binary for every node i.e 1 or 0 only.
- The library is helpful in constructing a directed network of nodes for given topography (say binary tree, ring, fully-connected, n-D cube etc).
- Each node on a graph receives input from multiple other nodes synchronously. All the inputs are processed using a PRE-OPERATOR that can be any symmertric operator (like AND, OR, XOR, 1, 0, NOR etc) to get an intermediate output.
- This indermediate output is then processed with the state of the node itself (i.e the value stored in the node which is also sent as output and received as input by its neighbour nodes) using a POST-OPERATOR which can be any of the 16 possible operators descibed below.

TRUTH TABLE:
| Y\X | 0 | 1 |
|-----|---|---|
| 0   | a | b |
| 1   | c | d |

 is operator abcd. Here X is the self-state of the node and Y is the intermediate output value of input signals.

It is noted that the phase transition and chaotic behaviour is observed not just in the Rule 30 and Rule 110 but also on other rule equivalents.

Here is a summary of some of the interesting cases that may be explored in depth in future.

PRE-OPERATOR, POST-OPERATOR --> Conclusion

binary_tree
	AND,	1010 --> Interesting case
	XOR, 	0001 --> Late congergence
	XOR, 	0101 --> Repetition of 32
	and other such cases under XOR
	OR, 	0101 --> Interesting case
fully_connected
	No intereting case. All cases converge fast to all 0's or repetition cycle 2.
ring
	AND, 	1010 --> Interesting case
	XOR, 	1010 --> Interesting case
	XOR, 	0011 --> Interesting case
	XOR, 	0101 --> Interesting case
	XOR, 	1010 --> Interesting case
	XOR, 	1100 --> Interesting case
	XOR, 	1101 --> Interesting case
	 OR, 	0101 --> Interesting case
teserract
	XOR, 	0001 --> Interesting case
	XOR, 	1000 --> Interesting case
	XOR, 	1011 --> Interesting case
	XOR, 	1101 --> Interesting case
  
A video has been uploaded explaining the operator on the input signals (PRE-OPERATOR) is XOR while the operator (POST-OPERATOR) on this output with node's own state is NOR. The video is Phase_Transition_in_F_XOR_G_1000_CA_Hypercube7.mp4

# PROJET_S3 (Othello)

The goal of the project is to program the "Othello/Reversi" game where two people can play together (on the same computer) or alone against the computer.

## Artificial Intelligence 
### feature-AI01
Implementation of a new heuristic function (v2.1)  
*Only worked for an 8x8 board*  
Result:  
- **90%** WR against the previous AI (v2.0 - Local Maximization) 
- **100%** against random pos AI

### feature-AI02
Implementation of a heuristic function (v3.3)  
*Works for every size of board*
Result:
- 8x8 : **80%** WR against random pos AI...
==> Aborted

### feature-AI03
Implementation of the ~~Minimax~~ AlphaBeta pruning algorithm with a dynamic heuristic function  
Result for *100 games*:  
- 4x4 : **97%** WR against random pos AI
- 6x6 : **100%** WR against random pos AI !
- 8x8 : **100%** WR against random pos AI !

## Various Size Board
### feature-VB01 
Change the whole project so it can handle a various-size board (v3.1)

## Clear Code 
### feature-REC01  
Increased readability, clearness and efficiency of the code (v3.2)

### feature-REC02
Multiple file organization

## Test  
### feature-T01
Test of multiple functions

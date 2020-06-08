# Robinson

Achieved:
1. So far it is able to detect the contradictory condition

To be fixed:
1. The Bound should not descent infinitely: 
I need to find a way of identify some positive or negative weighted bounds
    
   for example, the Within (self.U) table on (i,i) entry implies negatively weighted bounds, (i.e. $b$ negative bound,
    when doing some upperbounds $c$, $c - d*b$ for some constant $d$ is not a better upperbound) 
   
   Suppose there is Bounds us in U[i][i], then us is a positive bound. 
   Why?
   If it is a negative bound, then the distance of i to i is negative...
   
   The same rationale applies to L[i][i].
   
   In application, U[i][i] does not happen when one is adding two Tables,
   it happens when subtracting two tables, i.e. U[i][k] - L[j][k].
   In this case if L[i][k] is a negative bound, then we do not need to consider it.


# P080 OD3 Source Adjudication

OD3 exits cleanly with `ALL 8 CHECKS PASS`. The tally reproduces the source;
it does not establish its physical pin, consistency, or prediction headline.

The exact surviving operation is affine substitution. Starting from the
supplied design `[[2,0],[-4,0],[-1,k],[-2,2k]]`, assigning a value `y_pin` to
the second coordinate leaves the column `[2,-4,-1,-2]^T` and transforms the
right-hand side to `[g,m,h-k*y_pin,s-2*k*y_pin]^T`. This holds for every pin,
not specifically `1/(4*pi)`, and round-trips the original equations exactly.

The resulting coefficient rank is one, but that is only half the
classification. Its left nullspace has dimension three, giving
`2*g+m=0`, `g/2+h-k*y_pin=0`, and `g+s-2*k*y_pin=0`. Generic symbolic
right-hand sides have augmented rank two and are inconsistent. The remaining
coordinate is unique only after all three separately supplied compatibility
conditions hold. OD3.2 never inspects the right-hand side. OD3.5 solves the
gravity row and prints the other three forced left-hand sides, but never
compares them with their supplied equations; arbitrary mutations of those
rows leave its Boolean green.

The pin has no accepted physical provenance. C-SYM-002 makes `4*pi` only the
fixed coordinate of a separately supplied reciprocal map in one normalization
and does not require fixed-subfamily occupancy. A coordinate conjugation moves
that numeric fixed point. OD3's own opening correction instead declares
AS7's approximately 0.245 value physical, while its executable and output
continue to use `4*pi`; C-IDN-002 already classifies the AS7 value as an
input-conditioned inverse reconstruction. Thus neither value closes the pin.

The “no remaining freedom” language also fails its own data flow. The source
declares `b0` symbolic and uses `k=8*pi^2/b0`, so at the four-pi pin the folded
factor is `2*pi/b0`. The four offsets are symbolic and unproved. Treating them
as nuisance coordinates yields a rank-four design over five coordinates and
reopens the scale direction. C-GRV-001 additionally permits an additive
inverse-gravity baseline, which destroys the source's constant gravity log
slope outside the separately imposed zero-baseline branch. Other physical
sector rows remain pending or accepted only under narrower ceilings.

The exact affine, rank, compatibility, reference-shift, and conditional-solve
content is already owned by C-LIN-001 and C-IDN-001; P075's immutable AS4
adjudication already supplies the unpinned two-coordinate specialization. P080
therefore adds no claim or canonical API. OD3 is retained as
`duplicate_evidence` for those claims, while its physical pin, row
independence, absolute scale, causal freedom collapse, prediction, and maximal-
falsifiability readings are rejected.

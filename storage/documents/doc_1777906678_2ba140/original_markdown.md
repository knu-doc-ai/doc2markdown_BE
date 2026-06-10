# Automata and Formal Language (COMP315) Homework 1

Due date: 6th Apr. midnight (late submission not allowed) Submission: Upload a single PDF file that includes the answers Name:

Student ID:

### Q1. Language and Grammar

Given the grammar G below, compute the string 𝑤 for 𝑛= 3 and show the construction of 𝑤 using the sentential form.

아래의 문법 G에 대하여, n=3일 때의 문자열 w를 구하고, sentential form(문장형식)을 사용하여 w가 생성되는 과정을 보이시오.

𝐺= ({𝐴, 𝑆}, {𝑎, 𝑏}, 𝑆, 𝑃})

𝑃: 𝑆→𝑎𝐴𝑏|𝜆, 𝐴→𝑎𝐴𝑏|𝜆

𝐿(𝐺) = {𝑎!𝑏!: 𝑛≥0}

Answer:

### Q2. Grammar

Find the language 𝐿 for the grammar 𝐺= ({𝑆, 𝐴}, {𝑎, 𝑏}, 𝑆, 𝑃) that has the following production rules.

다음 생성 규칙을 갖는 문법 𝐺= ({𝑆, 𝐴}, {𝑎, 𝑏}, 𝑆, 𝑃)에 해당하는 언어 L을 구하시오.

𝑆→𝑎𝑎𝑏𝐴,

𝐴→𝑏𝑎𝑆,

Answer:

Q3. Chapter 1.2, Exercise 18 (pg. 29) Let 𝛴= {𝑎}. Find a grammar (production rules) for each language below. 아래의 각 언어에 대하여 문법(생성 규칙)을 구하시오

(a) 𝐿" = {𝑤: |𝑤|𝑚𝑜𝑑3 > 0}

Hint: Break down the problem into two cases, |𝑤|𝑚𝑜𝑑3 = 1 and |𝑤|𝑚𝑜𝑑3 =

힌트: |𝑤|𝑚𝑜𝑑3 = 1 인 경우와 |𝑤|𝑚𝑜𝑑3 = 2인 경우로 나누어 생각하시오.

Production rule(s) for 𝐿":

(b) 𝐿# = {𝑤: |𝑤|𝑚𝑜𝑑3 = 2}

Production rule(s) for 𝐿#:

### Q4. DFA

Show that 𝐿= {𝑎!: 0 ≤𝑛< 4} is regular, where Σ = {𝑎, 𝑏}.

Σ = {𝑎, 𝑏}일 때, 𝐿= {𝑎!: 0 ≤𝑛< 4} 언어가 정규 언어임을 보이시오.

Hint: A language 𝐿 is regular if you can construct a DFA for it.

힌트: 어떤 언어 L에 대해 DFA를 구성할 수 있으면, L은 정규 언어이다.

Answer:

### Q5. Write all the production rules of a grammar equivalent to the NFA below.

아래 NFA와 동등한 문법의 모든 생성 규칙을 쓰시오.

![Figure p3_figure_4](p3_picture_4.png)

![Figure p3_figure_5](p3_picture_5.png)

Q6. Draw the NFA for the transition functions defined below. Then, convert the NFA to a DFA. Here, the initial state=𝑞$ and the final state=𝑞#

아래에 정의된 전이 함수에 대한 NFA를 그리시오. 그런 다음, 이 NFA를 DFA로 변환하시오. 여기 서 시작 상태는 𝑞$, 종료 상태는 𝑞#이다.

𝛿(𝑞$, 𝑎) = {𝑞$, 𝑞", 𝑞#}

𝛿(𝑞", 𝑏) = {𝑞", 𝑞#}

𝛿(𝑞#, 𝑎) = {𝑞#}

𝛿(𝑞$, 𝜆) = {𝑞$, 𝑞#}

Answer:

### Q7. minimal DFA problem

(a) Write the transition functions 𝛿 for the NFA below. Also, convert the NFA into a DFA. 아래 NFA의 전이 함수 𝛿 들을 쓰시오. 또한 이 NFA를 DFA로 변환하시오.

![Figure p4_figure_4](p4_picture_4.png)

(b) For the converted DFA find an equivalent but minimal DFA. 변환된 DFA와 동등이며 상태 수가 최소인 DFA를 구하시오

(c) Find an equivalent grammar 𝐺 for the NFA in (a). Define the grammar as in G=(V,T,S,P). (a)의 NFA와 동등한 문법 G를 구하시오. 문법은 G=(V,T,S,P)의 형태로 정의하시오.

### Q8. NFA problem

Show that the language 𝐿= {𝑎} ∪{𝑐!: 𝑛≥3} is regular. 언어 𝐿= {𝑎} ∪{𝑐!: 𝑛≥3} 가 정규 언어임을 보이시오

Q9. Regular expression problem

(a) Find the regular expression of the language below. 아래 언어의 정규표현식을 구하시오.

𝐿= {𝑤∈{0,1}∗: 𝑤 𝑒𝑛𝑑𝑠 𝑤𝑖𝑡ℎ "10"}

## (b) Construct an NFA transition graph for the regular expression below. (Section 3.2, Exercise 3) 아래 정규표현식에 대한 NFA 전이 그래프를 구성하시오. (Section 3.2, Exercise 3)

𝑟= (𝑎𝑏∗+ 𝑏𝑏𝑎∗𝑎𝑏)

Q10. NFA problem, Chapter 2.3, Exercise 8

The language 𝑀= (𝑄, 𝛴, 𝛿, 𝑞$, 𝐹) is 𝐿(𝑀). The complement of 𝐿(𝑀) is 𝐿(𝑀). Discuss whether the following description of 𝐿(𝑀) SSSSSSS is true or false. 𝐿(𝑀) SSSSSSS = {𝑤∈𝛴∗: 𝛿∗(𝑞$, 𝑤) ∩𝐹= ∅}. 오토마타 𝑀= (𝑄, 𝛴, 𝛿, 𝑞$, 𝐹)의 언어를 L(M)라 하자. L(M)의 여집합은 𝐿(𝑀) SSSSSSS 이다. 다음과 같은 𝐿(𝑀) SSSSSSS. 의 설명이 참인지 거짓인지 논하시오. 𝐿(𝑀) SSSSSSS = {𝑤∈𝛴∗: 𝛿∗(𝑞$, 𝑤) ∩𝐹= ∅}.
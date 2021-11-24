from TexSoup import TexSoup

soup = TexSoup("""
\begin{document}

\section{Hello \textit{world}.}

\subsection{Watermelon}

(n.) A sacred fruit. Also known as:

\begin{itemize}
\item red lemon
\item life
\end{itemize}

Here is the prevalence of each synonym.

\begin{tabular}{c c}
red lemon & uncommon \\
life & common
\end{tabular}

\end{document}
""")

print(soup.section)
print(soup.section.name)
print(soup.section.string)
print(soup.tabular)


soup2 = TexSoup(open("E:\Studium\Semester_4\Data Science Projekt\TestCode\\acl2021.tex"))

print(soup2.section)

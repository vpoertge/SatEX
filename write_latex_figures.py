#this programme writes latex codes.
python_indices = ['TXx', 'TNx', 'TXn', 'TNn', 'DTR', 'FD', 'TR']


REGION = 'GERMANY'

with open('climpact_indices.txt', 'w') as f:
    for INAME in python_indices:
        f.write('\n\n\n')
        f.write('\\begin{figure*}\n\centering\n\\begin{subfigure}[b]{0.475\\textwidth}\n\centering\n')
        f.write('\\includegraphics[width=\\textwidth]{/scratch/vportge/plots/Python_Indices/min_LST_in_cold_window/'+REGION+'/'+INAME+'_map_of_trend_'+REGION+'.png}')
        f.write('\caption[]{{\small CM SAF LST}}\n\\end{subfigure}\n\hfill\n')

        f.write('\\begin{figure*}\n\centering\n\\begin{subfigure}[b]{0.475\\textwidth}\n\centering\n')
        f.write('\\includegraphics[width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+INAME+'_map_of_trend_'+REGION+'.png}')
        f.write('\caption[]{{\small GHCNDEX}}\n\\end{subfigure}\n\hfill\n')
        f.write('\\vskip\\baselineskip\n')

        f.write('\\begin{figure*}\n\centering\n\\begin{subfigure}[b]{0.475\\textwidth}\n\centering\n')
        f.write('\\includegraphics[width=\\textwidth]{/scratch/vportge/plots/Python_Indices/min_LST_in_cold_window/'+REGION+'/'+INAME+'_with_trend_ANN_'+REGION+'.png}')
        f.write('\caption[]{{\small CM SAF LST}}\n\\end{subfigure}\n\hfill\n')
        f.write('\quad\n')

        f.write('\\begin{figure*}\n\centering\n\\begin{subfigure}[b]{0.475\\textwidth}\n\centering\n')
        f.write('\\includegraphics[width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+INAME+'_time_series_GHCNDEX_with_trend_annually_'+REGION+'.png}')
        f.write('\caption[]{{\small GHCNDEX}}\n\\end{subfigure}\n')

        f.write('\caption[]\n{\small '+INAME+' }\n \label{fig:'+INAME+'}\n')
        f.write('\\end{figure*}')

'''
                {{\small CM SAF LST}}    
                %\label{fig:mean and std of net14}
        \end{subfigure}
        \hfill

        \begin{subfigure}[b]{0.475\textwidth}  
                \centering 
                \includegraphics[width=\textwidth]{/scratch/vportge/plots/GHCNDEX/GERMANY/TXn_map_of_trend_GERMANY.png}
                \caption[]%
                {{\small GHCNDEX }}    
                %\label{fig:mean and std of net24}
        \end{subfigure}
        \vskip\baselineskip
        \begin{subfigure}[b]{0.475\textwidth}   
                \centering 
                \includegraphics[width=\textwidth]{/scratch/vportge/plots/Python_Indices/min_LST_in_cold_window/GERMANY/TXn_with_trend_ANN_GERMANY.png}
                \caption[]%
                {{\small CM SAF LST}}    
                %\label{fig:mean and std of net34}
        \end{subfigure}
        \quad
        \begin{subfigure}[b]{0.475\textwidth}   
                \centering 
                \includegraphics[width=\textwidth]{/scratch/vportge/plots/GHCNDEX/GERMANY/TXn_time_series_GHCNDEX_with_trend_annually_GERMANY.png}
                \caption[]%
                {{\small GHCNDEX}}    
                %\label{fig:mean and std of net44}
        \end{subfigure}
        %\caption[ The average and standard deviation of critical parameters ]
        {\small TXn } 
        \label{fig:TXn}
\end{figure*}
'''
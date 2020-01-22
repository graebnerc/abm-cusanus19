#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 25 19:44:53 2018

@author: graebnerc
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def make_agg_plot(data_file, output_file):

    results = pd.read_feather(data_file)
    max_time = max(results["time"])
    
    results_grouped = results.groupby('time')
    results_plot = results_grouped.agg([np.mean, np.std])[["share_t0", "share_t1"]] 
    
    # The aggregated outpu
    fig, axes = plt.subplots(2, 1, figsize=(12,9)) # 2,1 means: two rows, one column of plots
    
    axes[0].spines["top"].set_visible(False) # Remove plot frame line on the top 
    axes[0].spines["right"].set_visible(False) # Remove plot frame line on the right
    
    axes[0].get_xaxis().tick_bottom() # ticks of x axis should only be visible on the bottom  
    axes[0].get_yaxis().tick_left()  # ticks of < axis should only be visible on the left  
    
    axes[0].yaxis.grid(color='grey',  # plot grid in grey
                  linestyle='-', # use normal lines
                  linewidth=1,   # the width should not be too much
                  alpha=0.45)    # transparent grids look better
    
    axes[0].fill_between(np.arange(0, max_time+1, 1), 
                    results_plot["share_t0"]["mean"]-results_plot["share_t0"]["std"], 
                    results_plot["share_t0"]["mean"]+results_plot["share_t0"]["std"], 
                    color="#3F5D7D")
    axes[0].plot(np.arange(0, max_time+1, 1), results_plot["share_t0"]["mean"], color="white", lw=2)
    axes[0].set_title("Average dynamics for technology 0")
    
    # Now the second subplot
    
    axes[1].spines["top"].set_visible(False) # Remove plot frame line on the top 
    axes[1].spines["right"].set_visible(False) # Remove plot frame line on the right
    
    axes[1].get_xaxis().tick_bottom() # ticks of x axis should only be visible on the bottom  
    axes[1].get_yaxis().tick_left()  # ticks of < axis should only be visible on the left  
    
    axes[1].yaxis.grid(color='grey',  # plot grid in grey
                  linestyle='-', # use normal lines
                  linewidth=1,   # the width should not be too much
                  alpha=0.45)    # transparent grids look better
    
    axes[1].fill_between(np.arange(0, max_time+1, 1), 
                    results_plot["share_t1"]["mean"]-results_plot["share_t1"]["std"], 
                    results_plot["share_t1"]["mean"]+results_plot["share_t1"]["std"], 
                    color="#cc6600")
    axes[1].plot(np.arange(0, max_time+1, 1), results_plot["share_t1"]["mean"], color="white", lw=2)
    axes[1].set_title("Average dynamics for technology 1")
    
    fig.suptitle('Overall results', fontsize=18)
    
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])

    plt.savefig(output_file, bbox_inches="tight")
    
    return True

#####

def make_disagg_plot(data_file, file_2):
    
    results = pd.read_feather(data_file)
    
    fig, axes = plt.subplots(2, 2, figsize=(12,9)) # 2,1 means: two rows, one column of plots
    
    # The first subplot 
    
    # full neighborhood, share 1
    results_full = results[results.neighborhood=="full"]
    results_ring = results[results.neighborhood=="ring"]
    max_id = max(results_full.id)
    
    
    axes[0,0].spines["top"].set_visible(False) # Remove plot frame line on the top 
    axes[0,0].spines["right"].set_visible(False) # Remove plot frame line on the right
    
    axes[0,0].get_xaxis().tick_bottom() # ticks of x axis should only be visible on the bottom  
    axes[0,0].get_yaxis().tick_left()  # ticks of < axis should only be visible on the left  
    
    axes[0,0].yaxis.grid(color='grey',  # plot grid in grey
                  linestyle='-', # use normal lines
                  linewidth=1,   # the width should not be too much
                  alpha=0.45)    # transparent grids look better
    
    for i in range(1, max_id+1):
        print(i)
        axes[0,0].plot(results_full[results_full.id==i].time, results_full[results_full.id==i].share_t0, lw=2, alpha=0.75)
    axes[0,0].set_title("Dynamics for technology 0 on the full network")
    
    # Now the second subplot
    
    axes[1,0].spines["top"].set_visible(False) # Remove plot frame line on the top 
    axes[1,0].spines["right"].set_visible(False) # Remove plot frame line on the right
    
    axes[1,0].get_xaxis().tick_bottom() # ticks of x axis should only be visible on the bottom  
    axes[1,0].get_yaxis().tick_left()  # ticks of < axis should only be visible on the left  
    
    axes[1,0].yaxis.grid(color='grey',  # plot grid in grey
                  linestyle='-', # use normal lines
                  linewidth=1,   # the width should not be too much
                  alpha=0.45)    # transparent grids look better
    
    min_id = min(results_ring.id)
    max_id = max(results_ring.id)
    
    for i in range(min_id, max_id+1):
        print(i)
        axes[1,0].plot(results_ring[results_ring.id==i].time, results_ring[results_ring.id==i].share_t0, lw=2, alpha=0.75)
    axes[1,0].set_title("Average dynamics for technology 0 on the ring")
    
    # The first subplot 
    
    # full neighborhood, share 1
    results_full = results[results.neighborhood=="full"]
    results_ring = results[results.neighborhood=="ring"]
    max_id = max(results_full.id)
    
    
    axes[0,1].spines["top"].set_visible(False) # Remove plot frame line on the top 
    axes[0,1].spines["right"].set_visible(False) # Remove plot frame line on the right
    
    axes[0,1].get_xaxis().tick_bottom() # ticks of x axis should only be visible on the bottom  
    axes[0,1].get_yaxis().tick_left()  # ticks of < axis should only be visible on the left  
    
    axes[0,1].yaxis.grid(color='grey',  # plot grid in grey
                  linestyle='-', # use normal lines
                  linewidth=1,   # the width should not be too much
                  alpha=0.45)    # transparent grids look better
    
    for i in range(1, max_id+1):
        print(i)
        axes[0,1].plot(results_full[results_full.id==i].time, results_full[results_full.id==i].share_t1, lw=2, alpha=0.75)
    axes[0,1].set_title("Dynamics for technology 1 on the full network")
    
    # Now the second subplot
    
    axes[1,1].spines["top"].set_visible(False) # Remove plot frame line on the top 
    axes[1,1].spines["right"].set_visible(False) # Remove plot frame line on the right
    
    axes[1,1].get_xaxis().tick_bottom() # ticks of x axis should only be visible on the bottom  
    axes[1,1].get_yaxis().tick_left()  # ticks of < axis should only be visible on the left  1
    axes[1,1].yaxis.grid(color='grey',  # plot grid in grey
                  linestyle='-', # use normal lines
                  linewidth=1,   # the width should not be too much
                  alpha=0.45)    # transparent grids look better
    
    min_id = min(results_ring.id)
    max_id = max(results_ring.id)
    
    for i in range(min_id, max_id+1):
        print(i)
        axes[1,1].plot(results_ring[results_ring.id==i].time, results_ring[results_ring.id==i].share_t1, lw=2, alpha=0.75)
    axes[1,1].set_title("Average dynamics for technology 1 on the ring")
    
    fig.suptitle('Overall results for the technology choice ABM', fontsize=18)
    
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    plt.savefig(file_2, bbox_inches="tight")
    
    return True

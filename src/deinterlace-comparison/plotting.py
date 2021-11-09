# for displaying the data
import matplotlib.pyplot as plt
# always need np
import numpy as np

def plot_image_difference(image_ground, image_di, title, show=True):
    fig, axs = plt.subplots(2, 3)

    fig.suptitle(title)

    axs[0,0].title.set_text('Ground truth')
    axs[0,1].title.set_text('Deinterlaced')
    axs[0,2].title.set_text('Difference')

    cmap_linear = 'gray'
    cmap_divergent = 'RdBu'

    image_ground_range = np.max(image_ground) - np.min(image_ground)
    image_diff = (image_di - image_ground) / image_ground_range

    diff_lims = np.max(np.abs([np.min(image_diff), np.max(image_diff)]))

    axs[0,0].imshow(image_ground, cmap=cmap_linear)
    axs[0,1].imshow(image_di, cmap=cmap_linear)
    im_diff_plot = axs[0,2].imshow(image_diff, vmin=-diff_lims, vmax=diff_lims, cmap=cmap_divergent)

    axs[1,0].imshow(image_ground, cmap=cmap_linear)
    axs[1,1].imshow(image_di, cmap=cmap_linear)
    axs[1,2].imshow(image_diff, vmin=-diff_lims, vmax=diff_lims, cmap=cmap_divergent)

    # sort out colour bar
    # box = axs.get_position()
    # axs.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    plt.subplots_adjust(bottom=0.05, right=0.88, top=0.85, left=0.02, wspace=0.02, hspace=0.02)
    # rect is x, y, width, height
    cax = plt.axes([0.90, 0.1, 0.03, 0.7])
    cbar = fig.colorbar(im_diff_plot, cax=cax)
    cbar.ax.tick_params(axis='y', direction='in', labelsize=8)

    for ax in axs[1, :]:
        ax.set_xlim([0, 50])
        ax.set_ylim([0, 50])

    for ax in axs.reshape(-1):
        ax.axis('off')

    if show:
        plt.show()
    else:
        plt.close(fig)


def plot_time_quality_graph(name, time, quality, time_n=1):

    fig, ax = plt.subplots(figsize=(9, 5))

    time_factor = 1000
    time_units = 'm'

    symbols = ['o', 's', '^', 'D', 'v', 'X', 'P']
    cols = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']

    s_n = len(symbols)
    c_n = len(cols)

    s_id = 0
    c_id = 0

    for i in range(len(name)):
        ax.scatter(time[i]*time_factor, quality[i], label=name[i], c=cols[c_id], marker=symbols[s_id])
        # ax.annotate(' ' + name[i], (time[i], quality[i]))

        c_id += 1

        if c_id == c_n:
            c_id = 0
            s_id += 1

            if s_id == s_n:
                s_id = 0

    ax.set_ylabel(f'Reconstruction quality')
    ax.set_xlabel(f'Average computation time, n={time_n} ({time_units}s)')

    ax.set_xscale('log')

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    plt.subplots_adjust(bottom=0.05, right=0.88, top=0.85, left=0.02, wspace=0.02, hspace=0.02)

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.tight_layout()

    plt.show()

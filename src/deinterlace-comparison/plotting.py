###############################################################################
#
# plotting.py
#
# Created by Jonathan J. P. Peters
#
# This fiel contains the functions for plotting the deinterlacing results, both
# images as well as speed/quality plots.
#
###############################################################################

# for displaying the data
import matplotlib.pyplot as plt
# always need np
import numpy as np
# to make our output folder if need be
import os


def plot_image_difference(image_ground, image_di, title, show=True, save_path=""):
    fig, axs = plt.subplots(2, 3, figsize=(7.5, 4.5), dpi=300)

    fig.suptitle(title, fontsize=10)

    axs[0, 0].set_title('Ground truth', fontsize=8)
    axs[0, 1].set_title('Deinterlaced', fontsize=8)
    axs[0, 2].set_title('Difference', fontsize=8)

    cmap_linear = 'gray'
    cmap_divergent = 'RdBu'

    image_ground_range = np.max(image_ground) - np.min(image_ground)
    image_diff_raw = (image_di - image_ground) / image_ground_range
    image_diff_pcnt = (image_di - image_ground) / image_ground_range

    # image_diff_raw = np.abs(image_diff_raw)
    # image_diff_pcnt = np.abs(image_diff_pcnt)

    im_min = np.min(image_ground)
    im_max = np.max(image_ground)

    # diff_lims = np.max(np.abs([np.min(image_diff), np.max(image_diff)]))
    diff_lims = 0.2

    axs[0, 0].imshow(image_ground, cmap=cmap_linear, vmin=im_min, vmax=im_max)
    axs[0, 1].imshow(image_di, cmap=cmap_linear, vmin=im_min, vmax=im_max)
    im_diff_plot = axs[0, 2].imshow(image_diff_pcnt, vmin=-diff_lims, vmax=diff_lims, cmap=cmap_divergent)

    ax_in00 = axs[0, 0].inset_axes(bounds=[0, 0.5, 0.5, 0.5])
    ax_in01 = axs[0, 1].inset_axes(bounds=[0, 0.5, 0.5, 0.5])
    ax_in02 = axs[0, 2].inset_axes(bounds=[0, 0.5, 0.5, 0.5])

    axs_in = [ax_in00, ax_in01, ax_in02]

    ax_in00.imshow(image_ground, cmap=cmap_linear, vmin=im_min, vmax=im_max)
    ax_in01.imshow(image_di, cmap=cmap_linear, vmin=im_min, vmax=im_max)
    ax_in02.imshow(image_diff_pcnt, vmin=-diff_lims, vmax=diff_lims, cmap=cmap_divergent)

    ground_fft = np.fft.fftshift(np.fft.fft2(image_ground))
    di_fft = np.fft.fftshift(np.fft.fft2(image_di))
    diff_fft = np.fft.fftshift(np.fft.fft2(image_diff_raw))

    ground_ps = np.log(np.abs(ground_fft) + 1)
    di_ps = np.log(np.abs(di_fft) + 1)
    diff_ps = np.log(np.abs(diff_fft) + 1)

    ps_min = np.min(ground_ps)
    ps_max = np.max(ground_ps)

    axs[1, 0].imshow(ground_ps, cmap=cmap_linear, vmin=ps_min, vmax=ps_max)
    axs[1, 1].imshow(di_ps, cmap=cmap_linear, vmin=ps_min, vmax=ps_max)
    axs[1, 2].imshow(diff_ps, cmap=cmap_linear, vmin=0.0, vmax=7.5)

    # diff_ps = np.abs(ground_fft) - np.abs(di_fft)
    # axs[2, 2].imshow(diff_ps, cmap=cmap_divergent, vmin=-300000000, vmax=300000000)

    # sort out colour bar
    # box = axs.get_position()
    # axs.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    plt.subplots_adjust(bottom=0.025, right=0.88, top=0.925, left=0.02, wspace=0.02, hspace=0.02)
    # rect is x, y, width, height
    cax = plt.axes([0.90, 0.33, 0.02, 0.5])
    cbar = fig.colorbar(im_diff_plot, cax=cax)
    cbar.ax.tick_params(axis='y', direction='in', labelsize=8)

    for ax in axs_in:

        crop = int(image_ground.shape[0] / 10)
        ax.set_xlim([0, crop])
        ax.set_ylim([0, crop])

    for ax in axs_in:
        ax.axis('off')

    for ax in axs.reshape(-1):
        ax.axis('off')

    ax.set_ylabel('V')
    ax.set_xlabel('t')

    if save_path:
        plt.savefig(os.path.join(save_path, f'{title}.pdf'))

    if show:
        plt.show()
    else:
        plt.close(fig)


def plot_time_quality_graph(name, time, quality, mcols, fcols, shps, time_n=1, show=True, save_path=""):

    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=100)

    time_factor = 1000
    time_units = 'm'

    ii = [i for i, x in enumerate(name) if x == 'NumPy Repeat']
    fac = 1 / quality[ii[0]]

    for i in range(len(name)):
        plot_kwargs = {}
        if fcols[i] is not None:
            plot_kwargs['markerfacecolor'] = fcols[i]
        if mcols[i] is not None:
            plot_kwargs['color'] = mcols[i]

        ax.plot(time[i]*time_factor, quality[i] * fac, markersize=4, label=name[i], marker=shps[i], **plot_kwargs)

    ax.set_ylabel(f'Reconstruction quality', fontsize=10)
    ax.set_xlabel(f'Average computation time, n={time_n} ({time_units}s)', fontsize=10)

    ax.tick_params(axis="y", direction="in", left="off", labelleft="on")

    ax.tick_params(axis='x', which='both', labelsize=8, direction="in")
    ax.tick_params(axis='y', which='both', labelsize=8, direction="in")
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')

    ax.set_xscale('log')
    # ax.set_yscale('log')

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    plt.subplots_adjust(bottom=0.05, right=0.88, top=0.85, left=0.02, wspace=0.02, hspace=0.02)

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 6}, frameon=False)

    plt.grid(which='both', color='#D0D0D0', linewidth=0.5)

    plt.tight_layout()

    if save_path:
        plt.savefig(os.path.join(save_path, 'time-quality.pdf'))

    if show:
        plt.show()
    else:
        plt.close(fig)

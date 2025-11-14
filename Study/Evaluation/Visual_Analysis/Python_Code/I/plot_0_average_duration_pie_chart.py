import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('fast')

df_a = pd.read_csv('average_duration_a.csv')
df_b = pd.read_csv('average_duration_b.csv')

labels_a = df_a['Duration Range']
sizes_a = df_a['Group A (%)']
labels_b = df_b['Duration Range']
sizes_b = df_b['Group B (%)']

colors = ['#1f77b4','#005491','#00316e','#2b83c0', '#73cbff']

fig1, ax1 = plt.subplots()
wedges, texts, autotexts = ax1.pie(sizes_a, labels=labels_a, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'color': 'black'})
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
ax1.axis('equal')
ax1.set_title("without interventions (A)")
fig1.savefig('plot_0_pie_a.png') 
plt.close(fig1)

fig2, ax2 = plt.subplots()
wedges, texts, autotexts = ax2.pie(sizes_b, labels=labels_b, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'color': 'black'})
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
ax2.axis('equal')
ax2.set_title("with interventions (B)")
fig2.savefig('plot_0_pie_b.png')
plt.close(fig2)

fig_combined, axs_combined = plt.subplots(1, 2, figsize=(10, 5))

wedges, texts, autotexts = axs_combined[0].pie(sizes_a, labels=labels_a, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'color': 'black'})
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
axs_combined[0].axis('equal')
axs_combined[0].set_title('without interventions (A)')

wedges, texts, autotexts = axs_combined[1].pie(sizes_b, labels=labels_b, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'color': 'black'})
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
axs_combined[1].axis('equal')
axs_combined[1].set_title('with interventions (B)')

fig_combined.suptitle("(e) Percentage Duration of Phone Uses\nwhile Social Interactions", fontweight= 'bold', fontsize=14)

plt.tight_layout()
fig_combined.savefig('plot_0_pie_a_b.png')
plt.close(fig_combined)



from tensorforce import Agent, Environment
import matplotlib.pyplot as plt
import numpy as np
import math
import pickle
from tqdm import tqdm

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

episode_number=100
evaluation_episode_number=5
average_over=10
length=np.zeros(episode_number)
measure_length=moving_average(length,average_over)

prohibition_parameter=[0,-10,-20,-30,-40,-50]
prohibition_position=[0.2,0.3,0.4,0.5]

reward_record_without=pickle.load(open( "without_record.p", "rb"))
evaluation_reward_record_without=pickle.load(open( "evaluation_without_record.p", "rb"))
reward_record_without_average=moving_average(reward_record_without,average_over)

reward_record_average=np.zeros((len(prohibition_position),len(prohibition_parameter),len(measure_length)))
reward_record=pickle.load(open( "record.p", "rb"))
for k in range(len(prohibition_position)):
    for i in range(len(prohibition_parameter)):
        reward_record_average[k][i]=moving_average(reward_record[k][i],average_over)

evaluation_reward_record=pickle.load(open( "evaluation_record.p", "rb"))
average_without=sum(evaluation_reward_record_without)/evaluation_episode_number
#plot training results
color_scheme=['yellowgreen','magenta','orange','blue','red','cyan','green']
x=range(len(measure_length))
for i in range(len(prohibition_position)):
    fig=plt.figure(figsize=(13,10))
    fig.suptitle('Prohibitive Boundary Position at %s \n Agents Trained Over %s Episodes \n Agents Evaluated Over %s Episodes' %(prohibition_position[i],episode_number,evaluation_episode_number),fontsize=16)
    plt.plot(x,reward_record_without_average,label='Normal Training \n Evaluation Average: \n %s' %average_without,color='black',linewidth=3,linestyle='-.')
    for j in range(len(prohibition_parameter)):
        average=0
        average=(sum(evaluation_reward_record[i][j])/evaluation_episode_number)
        plt.plot(x,reward_record_average[i][j],label='Parameter %s \n Evaluation Average: \n %s' %(prohibition_parameter[j],average),color=color_scheme[j])
    plt.xlabel('Episode Number', fontsize='xx-large', fontweight='bold')
    plt.ylabel('Episode Reward', fontsize='xx-large', fontweight='bold')
    plt.legend(loc='upper left',ncol=1, borderaxespad=0,prop={'size': 14})
    plt.savefig('Inverted_Pendulum_with_Boundary_at_%s_plot.png' %prohibition_position[i])

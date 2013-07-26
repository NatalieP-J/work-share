def InstantaneousPeriod(x):
    mod_x=#do something to time to get out period at that time
    return x

time=[some_array]

t_0=time[0]
P_0=InstantaneousPeriod(t_0)
t_n=time[-1]


t=t_0
while t<t_n:
    P_inst=InstantaneousPeriod(t)
    #call in signal information between t and t+P_inst as S
    S_fix=(P_0/P_inst)*S
    t+=P_inst

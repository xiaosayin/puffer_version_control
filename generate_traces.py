import pandas as pd
import numpy as np
import os

MEGA = 1000000
GIGA = 1000000000
save_folder = '/home/yinwenpei/raw_train_traces/train_traces/'
gap_time_stamps = 5   # > 5 seconds is the different traces
min_len_traces = 30   # trace_lenght > 30 as a trace

RAW_TRACES_FOLDER = '/home/yinwenpei/raw_train_traces/'
files_path = os.listdir(RAW_TRACES_FOLDER)
for files in files_path:
    # print(files)
    file_path = RAW_TRACES_FOLDER + files
    try:
        df = pd.read_csv(file_path)
    except:
        print(files)
        continue
    # time_stamps
    try:
        time_stamps = np.array(df['time (ns GMT)'])
    except:
        print(files)
        continue

    time_stamps = time_stamps / GIGA     # convert ns to seconds
    time_stamps = time_stamps - time_stamps[0] # start from 0
    # compute time_stamps cha_zhi
    dif_time_stamps = time_stamps[1:] - time_stamps[:-1]
    # gap_arg == index of jian ge
    gap_index = np.where(dif_time_stamps > gap_time_stamps)[0]
    # length of traces
    len_traces = gap_index[1:] - gap_index[:-1]
    index_traces = np.where(len_traces > min_len_traces)[0]
    low_size = gap_index[index_traces[0]] + 1
    high_size = gap_index[index_traces[0]+1]
    time_stamps_trace1 = time_stamps[gap_index[index_traces[0]]+1:gap_index[index_traces[0]+1]]
    time_stamps_trace1 = time_stamps_trace1 - time_stamps_trace1[0]
    # deliverate
    throughout = np.array(df['delivery_rate'])
    throughout = throughout * 8 / MEGA  # convert bytes/s to Mbit /s
    throughout_trace1 = throughout[low_size:high_size]
    # cwnd
    cwnd = np.array(df['cwnd'])
    cwnd_trace1 = cwnd[low_size:high_size]
    # in_flight
    in_flight = np.array(df['in_flight'])
    in_flight_trace1 = in_flight[low_size:high_size]
    # rtt
    rtt = np.array(df['rtt'])
    rtt = rtt / MEGA   # convert us to seconds
    rtt_trace1 = rtt[low_size:high_size]
    # min_rtt
    min_rtt = np.array(df['min_rtt'])
    min_rtt = min_rtt / MEGA   # convert us to seconds
    min_rtt_trace1 = min_rtt[low_size:high_size]

    # ensure the length equivalent
    assert len(throughout_trace1) == len(time_stamps_trace1)
    assert len(time_stamps_trace1) == len(cwnd_trace1)
    assert len(time_stamps_trace1) == len(in_flight_trace1)
    assert len(time_stamps_trace1) == len(rtt_trace1)
    assert len(time_stamps_trace1) == len(min_rtt_trace1)
    # write
    with open(save_folder + files[-17:-7]+'.log','w') as f:
        for i in range(len(time_stamps_trace1)):
            f.write(str(time_stamps_trace1[i]) + '\t' +
                    str(throughout_trace1[i]) + '\t' +
                    str(cwnd_trace1[i]) + '\t' +
                    str(in_flight_trace1[i]) + '\t' +
                    str(rtt_trace1[i]) + '\t' +
                    str(min_rtt_trace1[i]) + '\n')
            # print(i)
            if(i > 50):
                break





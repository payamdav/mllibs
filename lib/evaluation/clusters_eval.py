import numpy as np
import pandas as pd
import math


def evaluate_clusters_binary_labels(clusters, labels, out_df=False):
  # cluster has same length as labels
  # labels are binary just 0 and 1
  # clusters can be integers from 0 to n
  # both clusters and labels are np arrays
  # out is a dict with cluster number as key and dict as value with keys: count, 0, 1, 0_rate, 1_rate, count_rate
  out = {}
  for c in np.unique(clusters):
    cluster_labels = labels[clusters == c]
    count = len(cluster_labels)
    count_rate = count/len(labels)
    out[c] = {
      'count': count,
      '0': len(cluster_labels[cluster_labels == 0]),
      '1': len(cluster_labels[cluster_labels == 1]),
      '0_rate': len(cluster_labels[cluster_labels == 0])/count if count > 0 else 0,
      '1_rate': len(cluster_labels[cluster_labels == 1])/count if count > 0 else 0,
      'count_rate': count_rate
    }
  
  if out_df:
    return pd.DataFrame(out).T
  return out


def evaluate_clusters_binary_multi_labels(clusters, labels):
  clusters_numbers = np.sort(np.unique(clusters))
  labels_columns = labels.columns
  df = pd.DataFrame(index=clusters_numbers, columns=labels_columns, dtype=float)
  count = len(labels)
  for c in clusters_numbers:
    cluster_labels = labels[clusters == c]
    len_cluster = len(cluster_labels)
    for l in labels_columns:
      label_col = cluster_labels[l]
      df.loc[c, l] = len(label_col[label_col == 1])/len_cluster if len_cluster > 0 else 0
  return df

def evaluate_clusters_length(clusters):
  # clusters is np array
  clusters_numbers = np.sort(np.unique(clusters))
  df = pd.DataFrame(index=clusters_numbers, columns=['count', 'rate'])
  l = len(clusters)
  for c in clusters_numbers:
    count = len(clusters[clusters == c])
    df.loc[c, 'count'] = count
    df.loc[c, 'rate'] = count/l
  return df



def evaluate_clusters_binary_labels_chunk(clusters, labels, chunk=100):
  # same as evaluate_clusters_binary_labels but devide labels and clusters into chunks and return a dataframe
  columns = np.unique(clusters)
  df = pd.DataFrame(index=[i for i in range(math.ceil(len(labels)/chunk))], columns=columns)
  for i in range(math.ceil(len(labels)/chunk)):
    chunk_labels = labels[i*chunk:(i+1)*chunk]
    chunk_clusters = clusters[i*chunk:(i+1)*chunk]
    out = evaluate_clusters_binary_labels(chunk_clusters, chunk_labels, False)
    for c in columns:
      df.loc[i, c] = out[c]['1_rate'] if c in out else 0
  return df

    



import os
import pickle
import pandas as pd
from datetime import datetime
import os.path as osp
from preprocess_fn import ignore_first, only_keep_last, id_encode, remove_unseen_user_poi
import logging
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preprocessed_dir", type=str, required=True, help="Path to the directory containing the content of the unzipped file NYC.zip")
    parser.add_argument("--output_dir", type=str, required=True, help="Path to the directory where to save the data")
    
    args = parser.parse_args()
    return args


def preprocess_nyc(raw_path: bytes) -> pd.DataFrame:

    df_train = pd.read_csv(osp.join(raw_path, 'NYC_train.csv'))
    df_val = pd.read_csv(osp.join(raw_path, 'NYC_val.csv'))
    df_test = pd.read_csv(osp.join(raw_path, 'NYC_test.csv'))
    df_train['SplitTag'] = 'train'
    df_val['SplitTag'] = 'validation'
    df_test['SplitTag'] = 'test'
    df = pd.concat([df_train, df_val, df_test])
    df.columns = [
        'UserId', 'PoiId', 'PoiCategoryId', 'PoiCategoryCode', 'PoiCategoryName', 'Latitude', 'Longitude',
        'TimezoneOffset', 'UTCTime', 'UTCTimeOffset', 'UTCTimeOffsetWeekday', 'UTCTimeOffsetNormInDayTime',
        'pseudo_session_trajectory_id', 'UTCTimeOffsetNormDayShift', 'UTCTimeOffsetNormRelativeTime', 'SplitTag'
    ]

    # data transformation
    df['trajectory_id'] = df['pseudo_session_trajectory_id']
    df['UTCTimeOffset'] = df['UTCTimeOffset'].apply(lambda x: datetime.strptime(x[:19], "%Y-%m-%d %H:%M:%S"))
    df['UTCTimeOffsetEpoch'] = df['UTCTimeOffset'].apply(lambda x: x.strftime('%s'))
    df['UTCTimeOffsetWeekday'] = df['UTCTimeOffset'].apply(lambda x: x.weekday())
    df['UTCTimeOffsetHour'] = df['UTCTimeOffset'].apply(lambda x: x.hour)
    df['UTCTimeOffsetDay'] = df['UTCTimeOffset'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df['UserRank'] = df.groupby('UserId')['UTCTimeOffset'].rank(method='first')
    df = df.sort_values(by=['UserId', 'UTCTimeOffset'], ascending=True)

    # id encoding
    df['check_ins_id'] = df['UTCTimeOffset'].rank(ascending=True, method='first') - 1
    traj_id_le, padding_traj_id = id_encode(df, df, 'pseudo_session_trajectory_id')

    df_train = df[df['SplitTag'] == 'train']
    poi_id_le, padding_poi_id = id_encode(df_train, df, 'PoiId')
    poi_category_le, padding_poi_category = id_encode(df_train, df, 'PoiCategoryId')
    user_id_le, padding_user_id = id_encode(df_train, df, 'UserId')
    hour_id_le, padding_hour_id = id_encode(df_train, df, 'UTCTimeOffsetHour')
    weekday_id_le, padding_weekday_id = id_encode(df_train, df, 'UTCTimeOffsetWeekday')

    # ignore the first for train/validate/test and keep the last for validata/test
    df = ignore_first(df)
    df = only_keep_last(df)
    return df

def preprocess(preprocessed_dir, output_dir):
    dataset_name = 'nyc'
    data_path = ""
    preprocessed_path = output_dir
    sample_file = osp.join(preprocessed_path, 'sample.csv')
    train_file = osp.join(preprocessed_path, 'train_sample.csv')
    validate_file = osp.join(preprocessed_path, 'validate_sample.csv')
    test_file = osp.join(preprocessed_path, 'test_sample.csv')

    keep_cols = [
        'check_ins_id', 'UTCTimeOffset', 'UTCTimeOffsetEpoch', 'pseudo_session_trajectory_id',
        'query_pseudo_session_trajectory_id', 'UserId', 'Latitude', 'Longitude', 'PoiId', 'PoiCategoryId',
        'PoiCategoryName', 'last_checkin_epoch_time'
    ]

    if not osp.exists(preprocessed_path):
        os.makedirs(preprocessed_path)

    # Step 1. preprocess raw files and create sample files including
    # 1. data transformation; 2. id encoding; 3.train/validate/test splitting; 4. remove unseen user or poi
    if not osp.exists(sample_file):
        if 'nyc' == dataset_name:
            keep_cols += ['trajectory_id']
            preprocessed_data = preprocess_nyc(preprocessed_dir)

        preprocessed_result = remove_unseen_user_poi(preprocessed_data)
        preprocessed_result['sample'].to_csv(sample_file, index=False)
        preprocessed_result['train_sample'][keep_cols].to_csv(train_file, index=False)
        preprocessed_result['validate_sample'][keep_cols].to_csv(validate_file, index=False)
        preprocessed_result['test_sample'][keep_cols].to_csv(test_file, index=False)

if __name__ == '__main__':
    args = parse_args()
    preprocess(args.preprocessed_dir, args.output_dir)
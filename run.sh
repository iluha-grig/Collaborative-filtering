SOURCE_BASE_PATH="/collaborative_filtering"

INPUT_HADOOP_DIR="/collaborative_filtering/data/input"
OUTPUT_HADOOP_DIR="/collaborative_filtering/data/output"

HADOOP_STREAMING_PATH="${HADOOP_HOME}/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar"

hdfs dfs -test -d ${INPUT_HADOOP_DIR}
if [ $? -eq 0 ];
  then
    echo "Remove ${INPUT_HADOOP_DIR}"
    hdfs dfs -rm -r ${INPUT_HADOOP_DIR}
fi

hdfs dfs -test -d ${OUTPUT_HADOOP_DIR}
if [ $? -eq 0 ];
  then
    echo "Remove ${OUTPUT_HADOOP_DIR}"
    hdfs dfs -rm -r ${OUTPUT_HADOOP_DIR}
fi

test -d ${SOURCE_BASE_PATH}/data/output
if [ $? -eq 0 ];
  then
    echo "Remove ${SOURCE_BASE_PATH}/data/output"
    rm -rf ${SOURCE_BASE_PATH}/data/output
fi

hdfs dfs -mkdir -p ${INPUT_HADOOP_DIR}
hdfs dfs -copyFromLocal ${SOURCE_BASE_PATH}/data/input/* ${INPUT_HADOOP_DIR}


chmod 0777 ${SOURCE_BASE_PATH}/src/mapper1.py
chmod 0777 ${SOURCE_BASE_PATH}/src/reducer1.py
chmod 0777 ${SOURCE_BASE_PATH}/src/mapper2.py
chmod 0777 ${SOURCE_BASE_PATH}/src/reducer2.py
chmod 0777 ${SOURCE_BASE_PATH}/src/mapper3.py
chmod 0777 ${SOURCE_BASE_PATH}/src/reducer3.py
chmod 0777 ${SOURCE_BASE_PATH}/src/mapper4.py


hadoop_streaming_arguments_task_1="\
  -D mapred.reduce.tasks=16 \
  -files ${SOURCE_BASE_PATH}/src  \
  -mapper src/mapper1.py -reducer src/reducer1.py \
  -input ${INPUT_HADOOP_DIR}/ratings.csv -output ${OUTPUT_HADOOP_DIR}/stage_1 \
"

echo "Run streaming with arguments: \n${hadoop_streaming_arguments_task_1}"
hadoop jar ${HADOOP_STREAMING_PATH} ${hadoop_streaming_arguments_task_1}


hadoop_streaming_arguments_task_2="\
  -D mapred.reduce.tasks=16 \
  -files ${SOURCE_BASE_PATH}/src  \
  -mapper src/mapper2.py -reducer src/reducer2.py \
  -input ${OUTPUT_HADOOP_DIR}/stage_1/* -output ${OUTPUT_HADOOP_DIR}/stage_2 \
"

echo "Run streaming with arguments: \n${hadoop_streaming_arguments_task_2}"
hadoop jar ${HADOOP_STREAMING_PATH} ${hadoop_streaming_arguments_task_2}


hadoop_streaming_arguments_task_3="\
  -D mapred.reduce.tasks=16 \
  -files ${SOURCE_BASE_PATH}/src  \
  -mapper src/mapper3.py -reducer src/reducer3.py \
  -input ${OUTPUT_HADOOP_DIR}/stage_2/* -output ${OUTPUT_HADOOP_DIR}/stage_3 \
"

echo "Run streaming with arguments: \n${hadoop_streaming_arguments_task_3}"
hadoop jar ${HADOOP_STREAMING_PATH} ${hadoop_streaming_arguments_task_3}


hadoop_streaming_arguments_task_4="\
  -D mapred.reduce.tasks=1 \
  -files ${SOURCE_BASE_PATH}/src  \
  -mapper src/mapper4.py \
  -input ${OUTPUT_HADOOP_DIR}/stage_3/* -output ${OUTPUT_HADOOP_DIR}/final \
"

echo "Run streaming with arguments: \n${hadoop_streaming_arguments_task_4}"
hadoop jar ${HADOOP_STREAMING_PATH} ${hadoop_streaming_arguments_task_4}

hdfs dfs -copyToLocal ${OUTPUT_HADOOP_DIR}/final/part-00000 ${SOURCE_BASE_PATH}
mkdir ${SOURCE_BASE_PATH}/data/output
/collaborative_filtering/post_processor.py > ${SOURCE_BASE_PATH}/data/output/result.txt
rm ${SOURCE_BASE_PATH}/part-00000

echo "DONE! Result in /collaborative_filtering/data/output/result.txt"

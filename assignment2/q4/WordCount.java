package edu.stanford.cs246.wordcount;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Map.Entry;
import java.util.TreeMap;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class WordCount extends Configured implements Tool {
	public static void main(String[] args) throws Exception {
		System.out.println(Arrays.toString(args));
		int res = 0;
		for(int i = 0; i < 20; i++) {
			args[2] = Integer.toString(i);
			res = ToolRunner.run(new Configuration(), new WordCount(), args);
		}
		System.exit(res);
	}

	@Override
	public int run(String[] args) throws Exception {
		System.out.println(Arrays.toString(args));
		Job job = new Job(getConf(), "WordCount");

		int curr = Integer.parseInt(args[2]);
		int next = curr + 1;
		Configuration conf = job.getConfiguration();
		conf.set("inDir", "/home/cloudera/workspace/WordCount/data/res_" + curr + ".txt");
		conf.set("outDir", "/home/cloudera/workspace/WordCount/data/res_" + next + ".txt");
		conf.set("costDir", "/home/cloudera/workspace/WordCount/data/cost.txt");
		
		job.setJarByClass(WordCount.class);

		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);

		job.setMapperClass(Map.class);
		job.setReducerClass(Reduce.class);

		job.setMapOutputKeyClass(IntWritable.class);
		job.setMapOutputValueClass(Text.class);

		job.setInputFormatClass(TextInputFormat.class);
		job.setOutputFormatClass(TextOutputFormat.class);

		FileInputFormat.addInputPath(job, new Path(args[0]));			// need to change
		FileOutputFormat.setOutputPath(job, new Path(args[1] + curr));

		job.waitForCompletion(true);

		return 0;
	}

	private static double cost;
	
	public static class Map extends Mapper<LongWritable, Text, IntWritable, Text> {

		List<Double[]> centroids = new ArrayList<Double[]>();

		protected void setup(Context context) throws IOException, InterruptedException {
			cost = 0;
			// read file from inDir
			String fileName = context.getConfiguration().get("inDir");
			// read file by line
			File file = new File(fileName);
			BufferedReader reader = null;
			try {
				reader = new BufferedReader(new FileReader(file));
				String tempString = null;
				while ((tempString = reader.readLine()) != null) {
					String line = tempString;
					String[] centStr = line.trim().split("\\s");
					Double[] centDou = stringArray2DoubleArray(centStr);
					sanityCheck(centDou);
					centroids.add(centDou);
				}
				reader.close();
			} catch (IOException e) {
				e.printStackTrace();
			} finally {
				if (reader != null) {
					try {
						reader.close();
					} catch (IOException e1) {
					}
				}
			}
			// finished reading data
		}
		
		protected void cleanup(Context context) throws IOException, InterruptedException {
			String fileName = context.getConfiguration().get("costDir");
			try{
				FileWriter writer=new FileWriter(fileName, true);
				writer.write(cost + "\n");
				writer.close();
			} catch (IOException e)
			{
				e.printStackTrace();
			}
		}


//		double cost = 0;
		@Override
		public void map(LongWritable key, Text value, Context context)
				throws IOException, InterruptedException {
			String strVal = value.toString();
			String[] strArr = strVal.trim().split("\\s");
			Double[] point = stringArray2DoubleArray(strArr);
			double minDis = Double.MAX_VALUE;
			int index = -1;
			for(int i = 0; i < centroids.size(); i++) {
// =========================== here is the formula to compute distance ====================
//				double tmp = computeEudDis(point, centroids.get(i));
				double tmp = computeManDis(point, centroids.get(i));

				if(tmp < minDis) {
					minDis = tmp;
					index = i;
				}
			}

			context.write(new IntWritable(index), new Text(strVal));
			
			cost = cost + minDis;
			
		}
	}

	public static void sanityCheck(String[] str) {
		if(str.length != 58) {
			throw new RuntimeException("sanity failed");
		}
	}
	
	public static void sanityCheck(Double[] str) {
		if(str.length != 58) {
			throw new RuntimeException("sanity failed");
		}
	}
	
	public static Double[] stringArray2DoubleArray(String[] strArr) {
		Double[] ret = new Double[strArr.length];
		for(int i = 0; i < strArr.length; i++) {
			ret[i] = Double.parseDouble(strArr[i]);
		}
		return ret;
	}

	public static double computeEudDis(Double[] x, Double[] y) {
		double dis = 0;
		if(x.length != y.length) {
			throw new RuntimeException("Diff Length");
		}
		for(int i = 0; i < x.length; i++) {
			dis = dis + (x[i] - y[i]) * (x[i] - y[i]);
		}
		return dis;
	}
	
	public static double computeManDis(Double[] x, Double[] y){
		double dis = 0;
		if(x.length != y.length) {
			throw new RuntimeException("Diff Length");
		}
		for(int i = 0; i < x.length; i++) {
			dis = dis + Math.abs(x[i] - y[i]);
		}
		return dis;
	}


	public static class Reduce extends Reducer<IntWritable, Text, Text, Text> {


		@Override
		public void reduce(IntWritable key, Iterable<Text> values, Context context) throws IOException, InterruptedException {   	  
			double[] centerSum = new double[58];
			int centerCnt = 0;

			for(Text value : values) {
				centerCnt++;
				String strVal = value.toString();
				String[] strArr = strVal.trim().split("\\s");
				Double[] douArr = stringArray2DoubleArray(strArr);
				for(int i = 0; i < 58; i++) {
					centerSum[i] = centerSum[i] + douArr[i];
				}
			}

			double[] centerAvg = new double[58];
			for(int i = 0; i < 58; i++) {
				centerAvg[i] = centerSum[i] / centerCnt;
			}
			String res = "";
			for(int i = 0; i < 58; i++) {
				res = res + " " + Double.toString(centerAvg[i]);
			}
			String rest = res.substring(1);
			context.write(new Text(rest), new Text(""));

			String fileName = context.getConfiguration().get("outDir");
			try{
				FileWriter writer=new FileWriter(fileName, true);
				writer.write(rest + "\n");
				writer.close();
			} catch (IOException e)
			{
				e.printStackTrace();
			}

		}
	}
}
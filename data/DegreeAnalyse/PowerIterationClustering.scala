/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// scalastyle:off println
package org.apache.spark.examples.mllib

import org.apache.log4j.{Level, Logger}
import scopt.OptionParser

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.mllib.clustering.PowerIterationClustering
import java.io._
import org.apache.spark.rdd.RDD

/**
 * An example Power Iteration Clustering app.
 * http://www.cs.cmu.edu/~frank/papers/icml2010-pic-final.pdf
 * Takes an input of K concentric circles and the number of points in the innermost circle.
 * The output should be K clusters - each cluster containing precisely the points associated
 * with each of the input circles.
 *
 * Run with
 * {{{
 * ./bin/run-example mllib.PowerIterationClusteringExample [options]
 *
 * Where options include:
 *   k:  Number of circles/clusters
 *   n:  Number of sampled points on innermost circle.. There are proportionally more points
 *      within the outer/larger circles
 *   maxIterations:   Number of Power Iterations
 * }}}
 *
 * Here is a sample run and output:
 *
 * ./bin/run-example mllib.PowerIterationClusteringExample -k 2 --n 10 --maxIterations 15
 *
 * Cluster assignments: 1 -> [0,1,2,3,4,5,6,7,8,9],
 *   0 -> [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
 *
 * If you use it as a template to create your own app, please use `spark-submit` to submit your app.
 */
object PowerIterationClustering {

  case class Params(
      k: Int = 2,
      maxIterations: Int = 15,
      input: String = ""
    ) extends AbstractParams[Params]

  def main(args: Array[String]) {
    val defaultParams = Params()

    val parser = new OptionParser[Params]("PowerIterationClusteringExample") {
      head("PowerIterationClusteringExample: an example PIC app using concentric circles.")
      opt[Int]('k', "k")
        .text(s"number of circles (clusters), default: ${defaultParams.k}")
        .action((x, c) => c.copy(k = x))
      opt[Int]("maxIterations")
        .text(s"number of iterations, default: ${defaultParams.maxIterations}")
        .action((x, c) => c.copy(maxIterations = x))
      opt[String]("input")
        .text(s"input edgelist file")
        .action((x, c) => c.copy(input = x))
    }

    parser.parse(args, defaultParams) match {
      case Some(params) => run(params)
      case _ => sys.exit(1)
    }
  }

  def run(params: Params): Unit = {
    val conf = new SparkConf()
      .setMaster("local")
      .setAppName(s"PowerIterationClustering with $params")
    val sc = new SparkContext(conf)

    Logger.getRootLogger.setLevel(Level.WARN)

    // $example on$
    val edgeRdd = readEdgeList(sc, params.input)
    val startTime = System.currentTimeMillis()
    val model = new PowerIterationClustering()
      .setK(params.k)
      .setMaxIterations(params.maxIterations)
      .setInitializationMode("degree")
      .run(edgeRdd)
    val clusteringTime = System.currentTimeMillis() - startTime
    println(s"ToTalTrainingTime = ${clusteringTime} ms")

    val clusters = model.assignments.collect().groupBy(_.cluster).mapValues(_.map(_.id))
    val assignments = clusters.toList.sortBy { case (k, v) => v.length }
    val assignmentsStr = assignments
      .map { case (k, v) =>
        s"$k\t${v.sorted.mkString(",")}"
      }.mkString("\n")
    val sizesStr = assignments.map {
      _._2.length
    }.sorted.mkString("(", ",", ")")
    val writer = new PrintWriter(new File("ClusterResults/Results-"+System.currentTimeMillis()+".txt" ))
    writer.write(s"$assignmentsStr")
    // println(s"Cluster assignments: $assignmentsStr\n")
    println(s"Cluster sizes: $sizesStr")
    // $example off$

    sc.stop()
  }

  def readEdgeList(sc: SparkContext, filepath: String): RDD[(Long, Long, Double)] = {
    val lines = sc.textFile(filepath)
    lines.map(_.split(" "))
      .map(cols => {
        val src = cols(0).toLong
        val dst = cols(1).toLong
        val aff = cols(2).toDouble
        (src, dst, aff)
      })
  }


}
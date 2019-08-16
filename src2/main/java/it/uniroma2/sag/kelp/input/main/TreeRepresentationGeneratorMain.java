/*
 * Copyright 2018 Simone Filice and Giuseppe Castellucci and Danilo Croce and Roberto Basili
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package it.uniroma2.sag.kelp.input.main;

import edu.stanford.nlp.ie.machinereading.RelationFeatureFactory.DEPENDENCY_TYPE;
import it.uniroma2.sag.kelp.data.representation.tree.TreeRepresentation;
import it.uniroma2.sag.kelp.input.parser.DependencyParser;
import it.uniroma2.sag.kelp.input.parser.impl.StanfordParserWrapper2;
import it.uniroma2.sag.kelp.input.parser.model.DependencyGraph;
import it.uniroma2.sag.kelp.input.tree.TreeRepresentationGenerator;
import it.uniroma2.sag.kelp.input.tree.generators.LemmaCompactPOSLabelGeneratorLowerCase;
import it.uniroma2.sag.kelp.input.tree.generators.LexicalElementLabelGenerator;
import it.uniroma2.sag.kelp.input.tree.generators.OriginalPOSLabelGenerator;
import it.uniroma2.sag.kelp.input.tree.generators.PosElementLabelGenerator;
import it.uniroma2.sag.kelp.input.tree.generators.RelationNameLabelGenerator;
import it.uniroma2.sag.kelp.input.tree.generators.SyntElementLabelGenerator;
//import it.uniroma2.sag.kelp.kernel.tree.PartialTreeKernel;
//import it.uniroma2.sag.kelp.kernel.tree.SubTreeKernel;
import it.uniroma2.sag.kelp.kernel.tree.SubSetTreeKernel;
//import it.uniroma2.sag.kelp.kernel.tree.SmoothedPartialTreeKernel;
import java.io.*;

import java.util.ArrayList;
import java.util.List;

/**
 * Main class showing how to generate GRCT, LCT, CGRCT and CLCT representations
 * derived from a dependency graph produced by the Stanford Parser
 * 
 * More info about these representations can be found in:
 * 
 * - [Croce et al(2011)] Croce D., Moschitti A., Basili R. (2011) Structured
 * lexical similarity via convolution kernels on dependency trees. In:
 * Proceedings of EMNLP, Edinburgh, Scotland. <br>
 * <br>
 * - [Annesi et al(2014)] Paolo Annesi, Danilo Croce, and Roberto Basili. 2014.
 * Semantic compositionality in tree kernels. In Proc. of CIKM 2014, pages
 * 1029鈥�1038, New York, NY, USA. ACM
 * 
 * @author Danilo Croce
 * 
 */

public class TreeRepresentationGeneratorMain {
	public TreeRepresentation TreeRepresentationGen(String sentence){
		// Instantiate a new DependencyParser, i.e., a StanfordParser
		DependencyParser parser = new StanfordParserWrapper2(DEPENDENCY_TYPE.COLLAPSED);
		parser.initialize();
		// Initialize the label generators for: syntactic nodes, lexical nodes
		// and part-of-speech nodes
		SyntElementLabelGenerator rg = new RelationNameLabelGenerator();
		LexicalElementLabelGenerator ng = new LemmaCompactPOSLabelGeneratorLowerCase();
		PosElementLabelGenerator ig = new OriginalPOSLabelGenerator();

		// Parse a sentence
		DependencyGraph parse = parser.parse(sentence);		
		
		// Generating a Grammatical relation-centered Tree (GRCT).
		//TreeRepresentation grctTreeRepresentation = TreeRepresentationGenerator.grctGenerator(parse, rg, ng, ig);
		//print("GRCT", grctTreeRepresentation);
		//return grctTreeRepresentation;

		// Generating a Lexcial centered Tree (LCT).
		//TreeRepresentation lctTreeRepresentation = TreeRepresentationGenerator.lctGenerator(parse, rg, ng, ig);
		//print("LCT", lctTreeRepresentation);
		//return lctTreeRepresentation;

		// Generating a Compositionally Grammatical relation-centered Tree
		// (GRCT).
		//TreeRepresentation cgrctTreeRepresentation = TreeRepresentationGenerator.cgrctGenerator(parse, rg, ng, ig);
		//print("CGRCT", cgrctTreeRepresentation);
		//return cgrctTreeRepresentation;

		// Generating a Compositionally Lexical centered Tree (CLCT).
		TreeRepresentation clctTreeRepresentation = TreeRepresentationGenerator.clctGenerator(parse, rg, ng, ig);
		print("CLCT", clctTreeRepresentation);
		return clctTreeRepresentation;
	}

	private static void print(String repType, TreeRepresentation treeRepresentation) {
		String repString = treeRepresentation.getTextFromData();
		System.out.println(repType + "\t" + repString.replaceAll("\\(", "[").replaceAll("\\)", "]"));
		// System.out.println(repType +"\t"+ repString);
	}
	
	public float ptkComputation(String sentence1,String sentence2) {
		SubSetTreeKernel ptk = new SubSetTreeKernel(0.4f,"");
        TreeRepresentationGeneratorMain a = new TreeRepresentationGeneratorMain();
		TreeRepresentation a1 = a.TreeRepresentationGen(sentence1);
		TreeRepresentationGeneratorMain b = new TreeRepresentationGeneratorMain();
		TreeRepresentation b1 = b.TreeRepresentationGen(sentence2);	
		float initialPtk = ptk.kernelComputation(a1, b1);
		return initialPtk;
	}

	
	public static void method(String file, String conent) {
		BufferedWriter out = null;
		try {
		out = new BufferedWriter(new OutputStreamWriter(
		new FileOutputStream(file, true)));
		out.write(conent+"\r\n");
		} catch (Exception e) {
		e.printStackTrace();
		} finally {
		try {
		out.close();
		} catch (IOException e) {
		e.printStackTrace();
		}
		}
		}
	
	
	public static void main(String[] Args) {
		TreeRepresentationGeneratorMain ptk = new TreeRepresentationGeneratorMain();
		try {
			String pathname = "D:\\罗佳佳\\pycharm projects\\weizhongtrain.txt"; // 绝对路径或相对路径都可以，这里是绝对路径，写入文件时演示相对路径  
	        File filename = new File(pathname); // 要读取以上路径的input。txt文件  
	        InputStreamReader reader = new InputStreamReader(  
	                new FileInputStream(filename)); // 建立一个输入流对象reader  
	        BufferedReader br = new BufferedReader(reader); // 建立一个对象，它把文件内容转成计算机能读懂的语言  
	        String line = "";  
	        line = br.readLine(); 
	        int i = 1;
	        while (line != null) {  
         
	            System.out.println(line);
	            line = line.trim();
	            String a[] = line.split("\t");
	            String sent_left = a[1]; // 左边一句
	            String sent_right = a[1]; // 右边一句
	            System.out.println("左句为："+sent_left);
	            System.out.println("右句为："+sent_right);
	            String label = a[2];    //标签
	            line = br.readLine(); // 一次读入一行数据 
	            float ptk_value = ptk.ptkComputation(sent_left,sent_right);
	            System.out.println("ptk_value:"+ptk_value);
	            String piString = Float.toString(ptk_value);
	            //ArrayList ptk_value_list = new ArrayList();
	            //ptk_value_list.add(ptk_value);
	           
	            method("D:\\罗佳佳\\pycharm projects\\T2-T2-kernel\\ptk_value.txt", piString);
                if(i==5000){
                	break;
                }
                i = i+1;
	        }
		}
	        catch (Exception e){  

                e.printStackTrace();
		    }
	
	}
	
}

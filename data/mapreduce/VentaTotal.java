import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

// MapReduce: total vendido y numero de ventas por producto.
// Entrada: CSV de ventas (Cliente,Producto,Cantidad,PrecioUnitario,Anio,Mes,Ciudad,Monto)
public class VentaTotal {

    public static class TokenizerMapper extends Mapper<Object, Text, Text, DoubleWritable> {
        private Text producto = new Text();
        private DoubleWritable monto = new DoubleWritable();

        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {
            String linea = value.toString().trim();
            if (linea.isEmpty() || linea.startsWith("Cliente")) {
                return;
            }
            String[] campos = linea.split(",");
            if (campos.length < 8) {
                return;
            }
            try {
                producto.set(campos[1]);
                monto.set(Double.parseDouble(campos[7]));
                context.write(producto, monto);
            } catch (NumberFormatException e) {
                // fila invalida: se descarta
            }
        }
    }

    public static class SumReducer extends Reducer<Text, DoubleWritable, Text, Text> {
        public void reduce(Text key, Iterable<DoubleWritable> values, Context context)
                throws IOException, InterruptedException {
            double total = 0.0;
            int ventas = 0;
            for (DoubleWritable valor : values) {
                total += valor.get();
                ventas++;
            }
            context.write(key, new Text(String.format("%.2f\t%d", total, ventas)));
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "ventas total por producto");
        job.setJarByClass(VentaTotal.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setReducerClass(SumReducer.class);
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(DoubleWritable.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}

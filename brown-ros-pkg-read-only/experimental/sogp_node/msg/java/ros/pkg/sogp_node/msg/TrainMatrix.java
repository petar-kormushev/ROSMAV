/* auto-generated by genmsg_cpp from /home/iscander/ros/projects/sogp_node/msg/TrainMatrix.msg.  Do not edit! */
package ros.pkg.sogp_node.msg;


import java.nio.ByteBuffer;

public  class TrainMatrix extends ros.communication.Message
{

  public ros.pkg.sogp_node.msg.Matrix predictor;
  public ros.pkg.sogp_node.msg.Matrix target;

  public TrainMatrix() {
 super();
    predictor = new ros.pkg.sogp_node.msg.Matrix();
    target = new ros.pkg.sogp_node.msg.Matrix();

  }
  public static java.lang.String __s_getDataType() { return "sogp_node/TrainMatrix"; }
  public static java.lang.String __s_getMD5Sum() { return "9184cbeaeab8137e5760f8151a90613f"; }
  public static java.lang.String __s_getMessageDefinition()
  {
    return 
    "Matrix predictor\n" + 
    "Matrix target\n" + 
    "================================================================================\n" + 
    "MSG: sogp_node/Matrix\n" + 
    "Vector[] matrix_rows\n" + 
    "\n" + 
    "================================================================================\n" + 
    "MSG: sogp_node/Vector\n" + 
    "float32[] data\n" + 
    "\n" + 
    "\n" + 
    "";
  }
  public java.lang.String getDataType() { return __s_getDataType(); }
  public java.lang.String getMD5Sum()   { return __s_getMD5Sum(); }
  public java.lang.String getMessageDefinition() { return __s_getMessageDefinition(); }
  public TrainMatrix clone() {
    TrainMatrix clone = (TrainMatrix)super.clone();
      predictor = (ros.pkg.sogp_node.msg.Matrix)predictor.clone();
      target = (ros.pkg.sogp_node.msg.Matrix)target.clone();
    return clone;
  }

  public static java.util.Map<java.lang.String, java.lang.String> fieldTypes() {
         java.util.HashMap<java.lang.String, java.lang.String> m = new java.util.HashMap<java.lang.String, java.lang.String>  ();      m.put("predictor", "ros.pkg.sogp_node.msg.Matrix");
     m.put("target", "ros.pkg.sogp_node.msg.Matrix");
     return m;
  }

  public static java.util.Set<java.lang.String> submessageTypes() {
         java.util.HashSet<java.lang.String> s = new java.util.HashSet<java.lang.String>  ();      s.add("ros.pkg.sogp_node.msg.Matrix");
     s.add("ros.pkg.sogp_node.msg.Matrix");
     return s;
  }

  public void setTo(ros.communication.Message __m) {
    if (!(__m instanceof TrainMatrix)) throw new RuntimeException("Invalid Type");
    TrainMatrix __m2 = (TrainMatrix) __m;
    predictor = __m2.predictor;
    target = __m2.target;
    }

  public int serializationLength() 
  {
    int __l = 0;
    __l += predictor.serializationLength(); // predictor
    __l += target.serializationLength(); // target
    return __l;
  }
  public void serialize(ByteBuffer bb, int seq) {
     predictor.serialize(bb, seq);
     target.serialize(bb, seq);
  }
  public void deserialize(ByteBuffer bb)  {
     predictor.deserialize(bb);
     target.deserialize(bb);
  }
}


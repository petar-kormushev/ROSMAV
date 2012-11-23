/* auto-generated by gensrv_java from /home/snpucci/ros/brown-ros-pkg/experimental/pr2develop/joint_states_listener/srv/ReturnJointStates.srv.  Do not edit! */
package ros.pkg.joint_states_listener.srv;

import java.nio.ByteBuffer;

public class ReturnJointStates extends ros.communication.Service<ReturnJointStates.Request, ReturnJointStates.Response> 
{

public static String __s_getDataType() { return "joint_states_listener/ReturnJointStates"; }
public static String __s_getMD5Sum() { return "ce9bd2b56c904b190a782a08482fb4e9"; }

public String getDataType() { return ReturnJointStates.__s_getDataType(); }
public String getMD5Sum() { return ReturnJointStates.__s_getMD5Sum(); }

public static class Request extends ros.communication.Message
{

  public java.lang.String[] name;

  public Request() {
 super();
  name = new java.lang.String[0];

  }
  public static java.lang.String __s_getDataType() { return "joint_states_listener/ReturnJointStatesRequest"; }
  public static java.lang.String __s_getMD5Sum() { return ""; }
  public static java.lang.String __s_getMessageDefinition()
  {
    return 
    "string[] name\n" + 
    "\n" + 
    "";
  }
  public java.lang.String getDataType() { return __s_getDataType(); }
  public java.lang.String getMD5Sum()   { return __s_getMD5Sum(); }
  public java.lang.String getMessageDefinition() { return __s_getMessageDefinition(); }
  public static java.lang.String __s_getServerMD5Sum() { return ("ce9bd2b56c904b190a782a08482fb4e9"); }
  public java.lang.String getServerMD5Sum() { return __s_getServerMD5Sum(); }
  public static java.lang.String  __s_getServiceDataType() { return ("joint_states_listener/ReturnJointStates"); }
  public java.lang.String getServiceDataType() { return __s_getServiceDataType(); }
  public Request clone() {
    Request clone = (Request)super.clone();
      name =  (java.lang.String[])(clone.name.clone());
    return clone;
  }

  public static java.util.Map<java.lang.String, java.lang.String> fieldTypes() {
         java.util.HashMap<java.lang.String, java.lang.String> m = new java.util.HashMap<java.lang.String, java.lang.String>  ();      m.put("name", "java.lang.String[]");
     return m;
  }

  public static java.util.Set<java.lang.String> submessageTypes() {
         java.util.HashSet<java.lang.String> s = new java.util.HashSet<java.lang.String>  ();      return s;
  }

  public void setTo(ros.communication.Message __m) {
    if (!(__m instanceof Request)) throw new RuntimeException("Invalid Type");
    Request __m2 = (Request) __m;
    name = __m2.name;
    }

  int calc_name_array_serialization_len() {
    int l = 0;
    for (int i = 0; i < name.length; i++) 
      l += 4 + name[i].length();
    return l;
  }
  public int serializationLength() 
  {
    int __l = 0;
    __l += 4 + calc_name_array_serialization_len(); // name
    return __l;
  }
  public void serialize(ByteBuffer bb, int seq) {
    bb.putInt(name.length);
    for (java.lang.String x : name)
      Serialization.writeString(bb, x);
  }
  public void deserialize(ByteBuffer bb)  {
     int name_len = bb.getInt();
    name = new java.lang.String[name_len];
    for(int i = 0; i < name_len; i++)
      name[i] = Serialization.readString(bb);
  }
}

public static class Response extends ros.communication.Message
{

  public int[] found;
  public double[] position;
  public double[] velocity;
  public double[] effort;

  public Response() {
 super();
  found = new int[0];
  position = new double[0];
  velocity = new double[0];
  effort = new double[0];

  }
  public static java.lang.String __s_getDataType() { return "joint_states_listener/ReturnJointStatesResponse"; }
  public static java.lang.String __s_getMD5Sum() { return ""; }
  public static java.lang.String __s_getMessageDefinition()
  {
    return 
    "uint32[] found\n" + 
    "float64[] position\n" + 
    "float64[] velocity\n" + 
    "float64[] effort\n" + 
    "\n" + 
    "\n" + 
    "";
  }
  public java.lang.String getDataType() { return __s_getDataType(); }
  public java.lang.String getMD5Sum()   { return __s_getMD5Sum(); }
  public java.lang.String getMessageDefinition() { return __s_getMessageDefinition(); }
  public static java.lang.String __s_getServerMD5Sum() { return ("ce9bd2b56c904b190a782a08482fb4e9"); }
  public java.lang.String getServerMD5Sum() { return __s_getServerMD5Sum(); }
  public static java.lang.String  __s_getServiceDataType() { return ("joint_states_listener/ReturnJointStates"); }
  public java.lang.String getServiceDataType() { return __s_getServiceDataType(); }
  public Response clone() {
    Response clone = (Response)super.clone();
      found =  (int[])(clone.found.clone());
      position =  (double[])(clone.position.clone());
      velocity =  (double[])(clone.velocity.clone());
      effort =  (double[])(clone.effort.clone());
    return clone;
  }

  public static java.util.Map<java.lang.String, java.lang.String> fieldTypes() {
         java.util.HashMap<java.lang.String, java.lang.String> m = new java.util.HashMap<java.lang.String, java.lang.String>  ();      m.put("found", "int[]");
     m.put("position", "double[]");
     m.put("velocity", "double[]");
     m.put("effort", "double[]");
     return m;
  }

  public static java.util.Set<java.lang.String> submessageTypes() {
         java.util.HashSet<java.lang.String> s = new java.util.HashSet<java.lang.String>  ();      return s;
  }

  public void setTo(ros.communication.Message __m) {
    if (!(__m instanceof Response)) throw new RuntimeException("Invalid Type");
    Response __m2 = (Response) __m;
    found = __m2.found;
    position = __m2.position;
    velocity = __m2.velocity;
    effort = __m2.effort;
    }

  public int serializationLength() 
  {
    int __l = 0;
    __l += 4 + (found.length == 0 ? 0 : found.length * (4)); // found
    __l += 4 + (position.length == 0 ? 0 : position.length * (8)); // position
    __l += 4 + (velocity.length == 0 ? 0 : velocity.length * (8)); // velocity
    __l += 4 + (effort.length == 0 ? 0 : effort.length * (8)); // effort
    return __l;
  }
  public void serialize(ByteBuffer bb, int seq) {
    bb.putInt(found.length);
    bb.position(bb.position() + bb.asIntBuffer().put(found).position() * 4);
    bb.putInt(position.length);
    bb.position(bb.position() + bb.asDoubleBuffer().put(position).position() * 8);
    bb.putInt(velocity.length);
    bb.position(bb.position() + bb.asDoubleBuffer().put(velocity).position() * 8);
    bb.putInt(effort.length);
    bb.position(bb.position() + bb.asDoubleBuffer().put(effort).position() * 8);
  }
  public void deserialize(ByteBuffer bb)  {
     int found_len = bb.getInt();
    found = new int[found_len];
    bb.position(bb.position() + bb.asIntBuffer().get(found).position() * 4);
     int position_len = bb.getInt();
    position = new double[position_len];
    bb.position(bb.position() + bb.asDoubleBuffer().get(position).position() * 8);
     int velocity_len = bb.getInt();
    velocity = new double[velocity_len];
    bb.position(bb.position() + bb.asDoubleBuffer().get(velocity).position() * 8);
     int effort_len = bb.getInt();
    effort = new double[effort_len];
    bb.position(bb.position() + bb.asDoubleBuffer().get(effort).position() * 8);
  }
}

public ReturnJointStates.Request createRequest() { return new ReturnJointStates.Request(); }public ReturnJointStates.Response createResponse() { return new ReturnJointStates.Response(); }}

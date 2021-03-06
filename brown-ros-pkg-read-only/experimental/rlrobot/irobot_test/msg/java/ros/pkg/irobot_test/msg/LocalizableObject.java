/* auto-generated by genmsg_cpp from /home/sosentos/ros/brown-ros-pkg/trunk/experimental/rlrobot/irobot_test/msg/LocalizableObject.msg.  Do not edit! */
package ros.pkg.irobot_test.msg;


import java.nio.ByteBuffer;

public  class LocalizableObject extends ros.communication.Message
{

  public int objecttype;
  public int objectid;
  public double posx;
  public double posy;
  public double yaw;

  public LocalizableObject() {
 super();

  }
  public static java.lang.String __s_getDataType() { return "irobot_test/LocalizableObject"; }
  public static java.lang.String __s_getMD5Sum() { return "7d1f0aa2894b6168a0ed8aeafb7bd204"; }
  public static java.lang.String __s_getMessageDefinition()
  {
    return 
    "uint32 objecttype\n" + 
    "uint32 objectid\n" + 
    "float64 posx\n" + 
    "float64 posy\n" + 
    "float64 yaw\n" + 
    "\n" + 
    "\n" + 
    "";
  }
  public java.lang.String getDataType() { return __s_getDataType(); }
  public java.lang.String getMD5Sum()   { return __s_getMD5Sum(); }
  public java.lang.String getMessageDefinition() { return __s_getMessageDefinition(); }
  public LocalizableObject clone() {
    LocalizableObject clone = (LocalizableObject)super.clone();
    return clone;
  }

  public static java.util.Map<java.lang.String, java.lang.String> fieldTypes() {
         java.util.HashMap<java.lang.String, java.lang.String> m = new java.util.HashMap<java.lang.String, java.lang.String>  ();      m.put("objecttype", "int");
     m.put("objectid", "int");
     m.put("posx", "double");
     m.put("posy", "double");
     m.put("yaw", "double");
     return m;
  }

  public static java.util.Set<java.lang.String> submessageTypes() {
         java.util.HashSet<java.lang.String> s = new java.util.HashSet<java.lang.String>  ();      return s;
  }

  public void setTo(ros.communication.Message __m) {
    if (!(__m instanceof LocalizableObject)) throw new RuntimeException("Invalid Type");
    LocalizableObject __m2 = (LocalizableObject) __m;
    objecttype = __m2.objecttype;
    objectid = __m2.objectid;
    posx = __m2.posx;
    posy = __m2.posy;
    yaw = __m2.yaw;
    }

  public int serializationLength() 
  {
    int __l = 0;
    __l += 4; // objecttype
    __l += 4; // objectid
    __l += 8; // posx
    __l += 8; // posy
    __l += 8; // yaw
    return __l;
  }
  public void serialize(ByteBuffer bb, int seq) {
    bb.putInt(objecttype);
    bb.putInt(objectid);
    bb.putDouble(posx);
    bb.putDouble(posy);
    bb.putDouble(yaw);
  }
  public void deserialize(ByteBuffer bb)  {
    objecttype = bb.getInt();
    objectid = bb.getInt();
    posx = bb.getDouble();
    posy = bb.getDouble();
    yaw = bb.getDouble();
  }
}


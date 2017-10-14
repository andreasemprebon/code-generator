/**
 * Node Talk_List_Node
 * File auto-generated on 14/10/2017 13:10:25
 */
#include "ros_base/ROSNode.h"
#include "std_msgs/String.h"
#include "geometry_msgs/Point.h"
#define NODE_NAME "Talk_List_Node"

class Talk_List_Node : public ros_base::ROSNode {
private:
	bool prepare();
	void tearDown();
	void errorHandling();
	void call_pub_callback(const std_msgs::String::ConstPtr& msg);
	struct params {
		std::string stringName = "ciao";
		std::string nodeName = "NODE_NAME";
		double testReal = 0;
		bool testNoDefault;
	} params;
	struct vars {
		double publisherFrequency = 0;
		MyObject myObject;
	} vars;
	ros::Subscriber sub_call_pub;
	ros::Publisher pub_call_pub;
public:
	 Talk_List_Node();
};

/**
 * Method nodeSigintHandler auto-generated
 */
void nodeSigintHandler(int sig) {
	g_request_shutdown = 1;
}

/**
 * Method main auto-generated
 */
int main(int argc, char** argv) {
	ros::init(argc, argv, NODE_NAME, ros::init_options::NoSigintHandler);
	while(!ros::master::check())
		usleep(1000);
	signal(SIGINT, nodeSigintHandler);
	Talk_List_Node node;
	node.start();
	return 0;
}

/**
 * Method prepare auto-generated
 */
bool Talk_List_Node::prepare() {
	handle.param<std::string>("stringName", params.stringName, "ciao");
	handle.param<std::string>("nodeName", params.nodeName, "NODE_NAME");
	handle.param<double>("testReal", params.testReal, 0);
	handle.getParam("testNoDefault", params.testNoDefault);
	sub_call_pub = handle.subscribe("/in_topic", 1, &Talk_List_Node::call_pub_callback, this);
	pub_call_pub = handle.advertise < geometry_msgs::Point > ("/out_topic", 10);
	return true;
}

/**
 * Method tearDown auto-generated
 */
void Talk_List_Node::tearDown() {
	ROS_INFO("Node is shutting down");
	return;
}

/**
 * Method errorHandling auto-generated
 */
void Talk_List_Node::errorHandling() {
	ROSNode::errorHandling();
}

/**
 * Method call_pub_callback auto-generated
 */
void Talk_List_Node::call_pub_callback(const std_msgs::String::ConstPtr& msg) {
	ROS_INFO("%s", msg->data.c_str());
	/**
	 * Source text: talk_list.cpp
	 */
	
	pub_call_pub.publish(msg);
}

/**
 * Method Talk_List_Node auto-generated
 */
 Talk_List_Node::Talk_List_Node() {
	setName(NODE_NAME);
}


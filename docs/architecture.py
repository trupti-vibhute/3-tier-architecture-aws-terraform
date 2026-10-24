"""Generates docs/architecture.png using official AWS icons.

Requires Graphviz and the `diagrams` package:
    brew install graphviz
    pip install diagrams
    python docs/architecture.py
"""

from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2, EC2AutoScaling
from diagrams.aws.database import RDSPostgresqlInstance
from diagrams.aws.management import Cloudwatch
from diagrams.aws.network import ElbApplicationLoadBalancer, InternetGateway, NATGateway
from diagrams.aws.security import IAMRole, SecretsManager
from diagrams.aws.storage import SimpleStorageServiceS3Bucket
from diagrams.onprem.client import Users
from diagrams.onprem.container import Docker
from diagrams.onprem.iac import Terraform

OUT = Path(__file__).parent / "architecture"

graph_attr = {
    "fontsize": "24",
    "fontname": "Helvetica-Bold",
    "bgcolor": "white",
    "pad": "0.5",
    "nodesep": "0.9",
    "ranksep": "1.0",
    "splines": "ortho",
    "labelloc": "t",
}
node_attr = {"fontname": "Helvetica", "fontsize": "13"}


def cluster(color):
    return {"fontname": "Helvetica-Bold", "fontsize": "14", "margin": "22", "bgcolor": color, "pencolor": "#8c959f"}


request = Edge(color="#1f6feb", penwidth="2.2")
data = Edge(color="#1a7f37", penwidth="2.2")
support = Edge(color="#6e7781", style="dashed")
ops = Edge(color="#cf222e", style="dashed")

with Diagram(
    "Goal Tracker  -  AWS 3-Tier Architecture (Terraform)",
    filename=str(OUT),
    outformat="png",
    direction="LR",
    show=False,
    graph_attr=graph_attr,
    node_attr=node_attr,
):
    users = Users("Users")

    with Cluster("AWS Cloud  |  ap-south-1", graph_attr=cluster("#f6f8fa")):
        igw = InternetGateway("Internet\nGateway")

        with Cluster("VPC 10.0.0.0/16  |  spans 2 Availability Zones", graph_attr=cluster("#eef6ff")):
            with Cluster("Public Subnets", graph_attr=cluster("#e6f4ea")):
                public_alb = ElbApplicationLoadBalancer("Public ALB\nHTTP :80")
                bastion = EC2("Bastion Host")
                nat = NATGateway("NAT Gateway")

            with Cluster("Tier 1 - Presentation\nPrivate Subnets", graph_attr=cluster("#ffffff")):
                frontend = EC2AutoScaling("Frontend ASG\nNode.js  :3000\n2-4 x t3.micro")
                internal_alb = ElbApplicationLoadBalancer("Internal ALB\nHTTP :80")

            with Cluster("Tier 2 - Application\nPrivate Subnets", graph_attr=cluster("#ffffff")):
                backend = EC2AutoScaling("Backend ASG\nGo API  :8080\n2-6 x t3.micro")

            with Cluster("Tier 3 - Data\nIsolated Subnets", graph_attr=cluster("#ffffff")):
                rds = RDSPostgresqlInstance("RDS PostgreSQL 15\n:5432")

        with Cluster("Security & Operations", graph_attr=cluster("#fff8e6")):
            secrets = SecretsManager("Secrets Manager\nDB credentials")
            iam = IAMRole("IAM Role\n(SSM, Secrets)")
            cloudwatch = Cloudwatch("CloudWatch\nAlarms")
            state = SimpleStorageServiceS3Bucket("S3\nTerraform State")

    dockerhub = Docker("Docker Hub\nImages")
    terraform = Terraform("Terraform")
    admin = Users("Admin")

    # Request path
    users >> request >> igw >> request >> public_alb >> request >> frontend
    frontend >> request >> internal_alb >> request >> backend
    backend >> data >> rds

    # Supporting flows
    backend >> support >> secrets
    nat >> support >> dockerhub
    terraform >> support >> state

    # Operations access
    admin >> Edge(color="#cf222e", style="dashed", label="SSH :22") >> bastion

    # Lay out the security & operations services in a row instead of a column
    hidden = Edge(style="invis")
    state >> hidden >> iam >> hidden >> cloudwatch >> hidden >> secrets

import hello.world.HelloWorldPerformer;

class HelloWorldApp {
    public static void main(String[] args) {
        hello.world.HelloWorldPerformer.StaticInner.perform();
        new hello.world.HelloWorldPerformer().perform(); // Call method in instanciated HelloWorldPerformer.
    }
}

package hello.world;

public class HelloWorldPerformer {
    public static class StaticInner {
        public static void perform() {
            System.out.println("Hello World! (static)"); // Display the string.
        }
    }
    public class Inner {
        public void perform() {
            System.out.println("Hello World! (inner)"); // Display the string.
        }
    }
    public void perform() {
        Inner inner = new Inner();
        inner.perform();
    }
}
